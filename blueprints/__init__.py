from authlib.integrations.flask_client import OAuth   # type: ignore
from dotenv import load_dotenv   # type: ignore
import os 



oauth = OAuth() 
FACEBOOK_CLIENT_ID = os.getenv('facebook_client_id') 
FACEBOOK_CLIENT_SECRET = os.getenv('facebook_client_secret') 
GOOGLE_CLIENT_ID = os.getenv('google_client_id')  
GOOGLE_CLIENT_SECRET = os.getenv('google_client_secret') 


def create_oauth(app):
    """Configura os logins com Facebook e Google"""
    oauth.init_app(app)  # Prepara a ferramenta
    
    # Configura o Facebook
    oauth.register(
        name='facebook',
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        access_token_url='https://graph.facebook.com/oauth/access_token',
        authorize_url='https://www.facebook.com/dialog/oauth',
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )
    
    # Configura o Google
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        api_base_url='https://www.googleapis.com/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        client_kwargs={'scope': 'openid email profile'},
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs"
    )