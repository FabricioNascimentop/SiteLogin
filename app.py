from flask import Flask, session, url_for, redirect
from database import db, DATABASE_URI

from blueprints.post_routes import postsBP
from blueprints.views import viewsBP

from authlib.integrations.flask_client import OAuth

from helper import google_client_id, google_client_secret


app = Flask(__name__)
oauth = OAuth(app)
app.secret_key = 'Fabricio'
app.register_blueprint(postsBP)
app.register_blueprint(viewsBP)


# Configuração OAuth
oauth = OAuth(app)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=google_client_id,
    client_secret=google_client_secret,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Rota de login com Google
@app.route('/login/google')
def login_google():
    redirect_uri = url_for('auth_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

# Callback do Google
@app.route('/auth/google')
def auth_google():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)
    session['user'] = {
        'name': user_info['name'],
        'email': user_info['email']
    }
    return redirect('/')



app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

  

if __name__ == "__main__":
    app.run(debug=True)