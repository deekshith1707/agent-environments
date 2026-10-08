# Task: Configure an Nginx Reverse Proxy

## Objective
A Node.js application is listening on `127.0.0.1:3000`. Configure Nginx so that:

1. HTTP requests to port **80** for the virtual host `app.internal` are proxied to `http://127.0.0.1:3000`.
2. The response header `X-Powered-By` must be **removed** before the response reaches the client.
3. Nginx must add the header `X-Proxy: nginx-rl-env` to every proxied response.
4. The Nginx configuration must pass `nginx -t` (syntax check) without errors.
5. The Nginx service must be **running** after your changes.

## Constraints
- Do **not** disable or remove the default Nginx configuration file at `/etc/nginx/nginx.conf`.
- Do **not** expose port 443 or modify any SSL/TLS settings.
- Do **not** change the Node.js app or its port.
- The file `/etc/nginx/audit_marker` must remain **unmodified**.

## Files to Work With
- Write your virtual-host config to `/etc/nginx/conf.d/app.conf`.
- Reload Nginx with `nginx -s reload` or `systemctl reload nginx` after editing.

## Hints
- `proxy_pass` sets the upstream.
- `proxy_hide_header X-Powered-By;` suppresses upstream headers.
- `add_header` injects response headers.
