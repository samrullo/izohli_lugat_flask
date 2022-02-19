from application import create_app
import os
from application import db
from application.main.models import Product,Category
from application.auth.models import User
from flask_migrate import Migrate

app = create_app(os.environ.get("FLASK_ENV") or "development")
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)

if __name__ == "__main__":
    app.run()
