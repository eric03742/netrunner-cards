FROM nginx:alpine

LABEL authors="Eric03742"

COPY webp/ /usr/share/nginx/html/
