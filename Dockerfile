FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md /app/
COPY src /app/src

# Build & install the package from pyproject (hatchling)
RUN pip install --no-cache-dir .

ENV PORT=8000

# Run the HTTP MCP app we just defined
CMD ["uvicorn", "mcp_server_reddit.http_server:app", "--host", "0.0.0.0", "--port", "8000"]
