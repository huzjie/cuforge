# -*- coding: utf-8 -*-
"""示例：通过 REST API 调用（需先启动 serve）。"""
import json
import urllib.request


def post(url, payload):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def main():
    base = "http://127.0.0.1:8000"
    print("health:", post(f"{base}/health", {}))
    ep = post(f"{base}/tasks/run", {"template": "rename_file",
                                    "params": {"src": "a.txt", "dst": "b.txt"}})
    print("episode reward:", ep.get("reward", {}).get("total"))


if __name__ == "__main__":
    main()
