# ConvertImageToExcel

PDFやJPEGから文字認識し、Excelへ変換する

https://textdetector.murase-msk.work/

# 開発環境

- Windows10
- Windows Subsystem for Linux 2(Ubuntu20.04)
- Docker 20.10.7
  - docker-compose 1.26.0
    - app: Image: python:3.9.5-buster
    - db: Image: mysql:5.7
    - web Image: nginx:1.21.0
- Visual Studio Code
- Git
  - GitHub
  - SourceTree
- Python 3.9.5
  - Flask 2.0.1
  - SQLAlchemy 1.4.20
- Javascript, HTML, CSS
- Google Vision API

## 本番環境

- Google Cloud Platform
  - Google Compute Engine
