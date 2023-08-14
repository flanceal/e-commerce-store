# Nginx Configuration Examples

Here are example configuration blocks for Nginx, a web server, and reverse proxy. Replace placeholders with your own values.

## Nginx Server Block Configuration (`/etc/nginx/sites-available/{{your_site}}`)

```nginx
server {
    server_name {{your_server_name}};
    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias {{path_to_static_directory}};
    }
    location /media {
        alias {{path_to_media_directory}};
        access_log off;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate {{path_to_ssl_certificate}};
    ssl_certificate_key {{path_to_ssl_certificate_key}};
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam {{path_to_ssl_dhparam}}; # managed by Certbot
}

server {
    if ($host = {{your_host}}) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    server_name {{your_server_name}};
    listen 80;
    return 404; # managed by Certbot
}
```