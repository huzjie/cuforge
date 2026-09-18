# 部署

## Docker

```bash
docker build -t cuforge .
docker run --rm cuforge doctor
docker compose up -d     # 服务模式，暴露 8000
```

## Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml -f k8s/service.yaml
```

## 裸机

```bash
pip install -e ".[serve,yaml]"
python -m cuforge.cli.main serve --host 0.0.0.0 --port 8000
```
