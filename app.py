from flask import Flask
from database import db, DATABASE_URI

from blueprints.post_routes import postsBP
from blueprints.views import viewsBP

app = Flask(__name__)
app.secret_key = 'Fabricio'
app.register_blueprint(postsBP)
app.register_blueprint(viewsBP)




app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

  

if __name__ == "__main__":
    app.run(debug=True)