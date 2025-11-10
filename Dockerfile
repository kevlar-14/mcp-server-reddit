FROM python:3.11-slim

WORKDIR /app

# Copy project metadata and source
COPY pyproject.toml README.md /app/
COPY src /app/src

# Install this package (builds from pyproject.toml using hatchling)
# This is the standard pyproject build flow.
RUN pip install --no-cache-dir .

# Render will provide $PORT; default to 8000 for local runs
ENV PORT=8000

# Start the HTTP MCP server wrapper (the file we just added)
CMD ["python", "-m", "mcp_server_reddit.http_server"]
