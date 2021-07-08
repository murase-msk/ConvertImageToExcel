FROM nginx:1.21.0

ARG MAIL_ADDRESS

RUN apt-get update
RUN apt-get install -y certbot python3-certbot-nginx
RUN certbot certonly --agree-tos --standalone -d textdetector.murase-msk.work -m $MAIL_ADDRESS

CMD ["nginx", "-g", "daemon off;", "-c", "/etc/nginx/nginx.conf"]
