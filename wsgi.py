"""App entry point."""
from CompSciFlix import create_app

app = create_app()

if __name__ == "__main__":
    app.jinja_env.cache = {}
    app.run(host='localhost', port=5000, threaded=False)

