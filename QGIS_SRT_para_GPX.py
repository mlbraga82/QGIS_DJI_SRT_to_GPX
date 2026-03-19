import re
import os
from qgis.core import QgsProject, QgsVectorLayer
from qgis.PyQt.QtWidgets import QFileDialog, QMessageBox
from qgis.utils import iface

def processar_dji_srt():
    # 1. Seleção do Arquivo
    arquivo_srt, _ = QFileDialog.getOpenFileName(
        None, "Selecionar Arquivo SRT da DJI", "", "Arquivos SRT (*.srt)"
    )
    
    if not arquivo_srt:
        return

    nome_base, _ = os.path.splitext(arquivo_srt)
    caminho_gpx = nome_base + ".gpx"
    
    try:
        with open(arquivo_srt, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        # Separação por blocos de legenda
        blocos = [b for b in conteudo.split('\n\n') if b.strip()]
        gpx_points = []

        for bloco in blocos:
            # Regex específicas para o formato Mavic 3T enviado
            lat_match = re.search(r'\[latitude:\s*([\d\.-]+)\]', bloco)
            lon_match = re.search(r'\[longitude:\s*([\d\.-]+)\]', bloco)
            
            # Captura o valor após 'abs_alt:' mesmo dentro de um bloco compartilhado
            alt_match = re.search(r'abs_alt:\s*([\d\.-]+)', bloco)
            
            # Captura a data e hora (Ex: 2026-03-10 15:21:01.462)
            data_hora_match = re.search(r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})', bloco)

            if lat_match and lon_match:
                lat, lon = lat_match.group(1), lon_match.group(1)
                # Usa abs_alt se encontrado, senão 0
                alt = alt_match.group(1) if alt_match else "0"
                dt_str = data_hora_match.group(1).replace(" ", "T") + "Z" if data_hora_match else "2026-01-01T00:00:00Z"

                gpx_points.append(
                    f'      <trkpt lat="{lat}" lon="{lon}">\n'
                    f'        <ele>{alt}</ele>\n'
                    f'        <time>{dt_str}</time>\n'
                    f'      </trkpt>'
                )

        # Geração do GPX
        cabecalho = '<?xml version="1.0" encoding="UTF-8"?>\n<gpx version="1.1" creator="QGIS_DJI">\n  <trk>\n    <name>Voo Drone</name>\n    <trkseg>\n'
        rodape = '\n    </trkseg>\n  </trk>\n</gpx>'
        
        with open(caminho_gpx, 'w', encoding='utf-8') as f:
            f.write(cabecalho + '\n'.join(gpx_points) + rodape)

        # 2. Importação no QGIS
        uri = caminho_gpx + "|layername=track_points"
        camada = QgsVectorLayer(uri, os.path.basename(caminho_gpx), "ogr")
        
        if not camada.isValid():
            QMessageBox.critical(None, "Erro", "Falha ao carregar os pontos GPX.")
            return

        QgsProject.instance().addMapLayer(camada)
        iface.mapCanvas().setExtent(camada.extent())
        iface.mapCanvas().refresh()
        
        QMessageBox.information(None, "Sucesso", f"Importação concluída!\nAltitude extraída: {alt}m (exemplo do último ponto).")

    except Exception as e:
        QMessageBox.critical(None, "Erro", f"Erro: {str(e)}")

processar_dji_srt()
