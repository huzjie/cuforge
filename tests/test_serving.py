# -*- coding: utf-8 -*-
def test_create_app():
    try:
        from cuforge.serving.app import create_app
        app = create_app()
        assert app.title == "cuforge"
    except ImportError:
        pass  # fastapi 未安装时跳过
