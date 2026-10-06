from wsgiref.simple_server import make_server

from .web import create_seeded_app


if __name__ == "__main__":
    app = create_seeded_app()
    with make_server("127.0.0.1", 8000, app) as server:
        print(
            "RelayBoard listening on "
            "http://127.0.0.1:8000/dashboard"
        )
        server.serve_forever()
