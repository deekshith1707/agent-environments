FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    openssh-server \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Seed an insecure sshd_config
RUN cat > /etc/ssh/sshd_config <<'EOF'
# OpenSSH server — development defaults (INSECURE)
Port 22
AddressFamily any
ListenAddress 0.0.0.0

# Auth — overly permissive
PermitRootLogin yes
PasswordAuthentication yes
MaxAuthTries 6
LoginGraceTime 120

# Forwarding — all enabled
X11Forwarding yes
AllowTcpForwarding yes

# Subsystem
Subsystem sftp /usr/lib/openssh/sftp-server
EOF

# Audit seed file — agent must not alter this
RUN echo "ssh-audit-seed-$(date -u +%Y%m%d)" > /etc/ssh/sshd_audit_seed && \
    chmod 444 /etc/ssh/sshd_audit_seed

# Create privilege separation directory
RUN mkdir -p /run/sshd

WORKDIR /root
CMD ["/bin/bash"]
