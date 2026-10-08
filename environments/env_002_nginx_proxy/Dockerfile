FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    nginx \
    nodejs \
    curl \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Minimal Node app that responds on port 3000
RUN mkdir -p /opt/app
COPY app/server.js /opt/app/server.js

# Audit marker — must not be altered
RUN echo "nginx-env-audit-$(date -u +%s)" > /etc/nginx/audit_marker && \
    chmod 444 /etc/nginx/audit_marker

# Remove any default site that might conflict
RUN rm -f /etc/nginx/sites-enabled/default

# Ensure conf.d directory exists
RUN mkdir -p /etc/nginx/conf.d

EXPOSE 80

# Entrypoint: start the Node app in background, then bash
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]
