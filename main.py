from application import create_app
import os

app = create_app(os.environ.get("FLASK_ENV") or "development")

if __name__ == "__main__":
    app.run()
