FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    python3 \
    # TODO: add packages
    && rm -rf /var/lib/apt/lists/*

# TODO: Create initial filesystem state
# RUN mkdir -p /some/path && echo "seed" > /some/path/file

# Immutable audit file — agent must not touch this
RUN echo "audit-seed-$(date -u +%s)" > /etc/template_audit && \
    chmod 444 /etc/template_audit

WORKDIR /root
CMD ["/bin/bash"]
