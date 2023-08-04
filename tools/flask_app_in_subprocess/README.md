# 在子进程中使用 gevent.pywsgi   WSGIServer 运行 flask服务

## 关键代码
只有在子进程运行时中导入 app,
才能是的 app 在子进程中完成一些本地变量的初始化

```python
def run_app():
    """
    只有在子进程运行时中导入 app
    """
    from flask_app_in_subprocess.server import app
    from gevent.server import _tcp_listener

    listener = _tcp_listener(('0.0.0.0', 5004))
    wsgi_server = WSGIServer(listener, app)
    wsgi_server.serve_forever()
```
