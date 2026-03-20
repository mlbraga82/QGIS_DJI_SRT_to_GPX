# QGIS_DJI_SRT_to_GPX

DJI SRT to QGIS GPX Converter (Python Script)
Este script Python foi desenvolvido para facilitar o fluxo de trabalho de inteligência geográfica e análise de voos. Ele extrai dados de telemetria contidos em arquivos .srt gerados por drones DJI (testado extensivamente com DJI Mavic 3T) e os converte em um arquivo .gpx pronto para uso no QGIS.
🚀 Funcionalidades

    Interface Gráfica Nativa: Abre uma janela de seleção de arquivos diretamente no QGIS.
    Preservação de Dados: O arquivo .srt original não é alterado; um novo arquivo .gpx é criado no mesmo diretório.
    Extração de Alta Precisão:
        Coordenadas: Latitude e Longitude de cada frame.
        Altitude Absoluta (abs_alt): Extrai a altitude em relação ao nível do mar (MSL), essencial para análises topográficas.
        Timestamp Real: Mantém a data e hora exata (com milissegundos) de cada ponto do voo.
    Importação Automática: Adiciona a camada de pontos (track_points) ao projeto atual do QGIS e ajusta o zoom automaticamente para a área de interesse.

🛠️ Como Usar

    Abra o seu projeto no QGIS.
    Vá em Complementos > Console Python (ou pressione Ctrl + Alt + P).
    Clique no ícone de Editor (o botão que parece um bloco de notas).
    Cole o código do script e clique no botão Executar Script (ícone de "Play" verde).
    Selecione o arquivo .srt desejado na janela que será aberta.
    [atualização:]
    Foi acrecentado o arquivo QGIS_SRT_para_GPX_processing.py para utilizar como script no Processing (Caixa de Ferramentas de Processamento)

⚖️ Requisitos

    QGIS 3.x (com as bibliotecas PyQt5 e qgis.core nativas).
    Arquivos SRT gerados por drones DJI com telemetria habilitada.
