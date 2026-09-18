FROM python:3.11-slim

WORKDIR /app

# 先装依赖（服务模式需要 fastapi/uvicorn）
RUN pip install --no-cache-dir fastapi "uvicorn[standard]" pydantic PyYAML

COPY . /app
RUN pip install --no-cache-dir -e .

EXPOSE 8000

ENV CUFORGE_CONFIG=config.yaml

CMD ["python", "-m", "cuforge.cli.main", "serve", "--host", "0.0.0.0", "--port", "8000"]
