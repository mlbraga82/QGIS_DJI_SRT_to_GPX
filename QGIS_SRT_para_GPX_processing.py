import re
import os
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterFileDestination,
                       QgsVectorLayer,
                       QgsProject)

class DJI_SRT_To_GPX(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return DJI_SRT_To_GPX()

    def name(self):
        return 'dji_srt_to_gpx'

    def displayName(self):
        return self.tr('Converter DJI SRT para GPX')

    def group(self):
        return self.tr('Scripts DJI')

    def groupId(self):
        return 'scripts_dji'

    def shortHelpString(self):
        return self.tr('Extrai coordenadas e altitude de arquivos SRT da DJI (Mavic 3T) e gera uma camada GPX.')

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                self.tr('Arquivo SRT de entrada'),
                extension='srt'
            )
        )
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr('Salvar arquivo GPX como'),
                fileFilter='Arquivos GPX (*.gpx)'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        arquivo_srt = self.parameterAsFile(parameters, self.INPUT, context)
        caminho_gpx = self.parameterAsFileOutput(parameters, self.OUTPUT, context)

        try:
            with open(arquivo_srt, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            blocos = [b for b in conteudo.split('\n\n') if b.strip()]
            gpx_points = []

            for i, bloco in enumerate(blocos):
                # Feedback de progresso
                feedback.setProgress(int((i / len(blocos)) * 100))
                
                if feedback.isCanceled():
                    break

                lat_match = re.search(r'\[latitude:\s*([\d\.-]+)\]', bloco)
                lon_match = re.search(r'\[longitude:\s*([\d\.-]+)\]', bloco)
                alt_match = re.search(r'abs_alt:\s*([\d\.-]+)', bloco)
                data_hora_match = re.search(r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})', bloco)

                if lat_match and lon_match:
                    lat = lat_match.group(1)
                    lon = lon_match.group(1)
                    alt = alt_match.group(1) if alt_match else "0"
                    dt_str = data_hora_match.group(1).replace(" ", "T") + "Z" if data_hora_match else "2026-01-01T00:00:00Z"

                    gpx_points.append(
                        f'      <trkpt lat="{lat}" lon="{lon}">\n'
                        f'        <ele>{alt}</ele>\n'
                        f'        <time>{dt_str}</time>\n'
                        f'      </trkpt>'
                    )

            # Geração do arquivo GPX
            cabecalho = '<?xml version="1.0" encoding="UTF-8"?>\n<gpx version="1.1" creator="QGIS_DJI">\n  <trk>\n    <name>Voo Drone</name>\n    <trkseg>\n'
            rodape = '\n    </trkseg>\n  </trk>\n</gpx>'
            
            with open(caminho_gpx, 'w', encoding='utf-8') as f:
                f.write(cabecalho + '\n'.join(gpx_points) + rodape)

            # Carregar a camada no QGIS
            uri = caminho_gpx + "|layername=track_points"
            camada = QgsVectorLayer(uri, os.path.basename(caminho_gpx), "ogr")
            
            if camada.isValid():
                QgsProject.instance().addMapLayer(camada)

            return {self.OUTPUT: caminho_gpx}

        except Exception as e:
            feedback.reportError(f"Erro ao processar: {str(e)}")
            return {}
