# base image
FROM python:3.9.5-buster

# 変数定義
ARG project_dir /var/www/ConvertImageToExcel/

# workdir にファイル等追加
ADD requirements.txt $project_dir

# workdir
# なければ新規作成
WORKDIR $project_dir

#port
# EXPOSE 3031

#環境変数設定
ENV PORT=80
ENV PYTHONUNBUFFERED=1

RUN apt-get update
# upgrade pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# PDF image 変換
RUN apt-get install -y poppler-utils

# mysql client
RUN apt-get install -y default-mysql-client

# uwsgi設定
CMD ["uwsgi","--ini","/var/www/ConvertImageToExcel/build/app/uwsgi.ini"]
