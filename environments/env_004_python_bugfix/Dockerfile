FROM python:3.11-slim

RUN pip install --no-cache-dir pytest

# Create package layout
RUN mkdir -p /opt/dataproc/dataproc /opt/dataproc/tests

# Package init
RUN touch /opt/dataproc/dataproc/__init__.py

# Buggy aggregator module
COPY app/aggregator.py /opt/dataproc/dataproc/aggregator.py

# Existing tests (must all pass after the fix)
COPY app/test_aggregator.py /opt/dataproc/tests/test_aggregator.py
RUN touch /opt/dataproc/tests/__init__.py

# Minimal pyproject
RUN cat > /opt/dataproc/pyproject.toml <<'TOML'
[project]
name = "dataproc"
version = "0.1.0"
TOML

WORKDIR /opt/dataproc
CMD ["/bin/bash"]
