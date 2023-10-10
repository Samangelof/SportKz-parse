from flask import Flask, redirect, request, url_for, session
from requests_oauthlib import OAuth2Session
from route import route_bp
import os


app = Flask(__name__)

app.register_blueprint(route_bp)




app.config['FACEBOOK_APP_ID'] = ''
app.config['FACEBOOK_APP_SECRET'] = ''


secret_key = os.urandom(24)
app.secret_key = secret_key


FACEBOOK_API_URL = 'https://graph.facebook.com/v11.0/'


@app.route('/login')
def login():
    facebook = OAuth2Session(app.config['FACEBOOK_APP_ID'])
    authorization_url, state = facebook.authorization_url('https://www.facebook.com/dialog/oauth')
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    facebook = OAuth2Session(app.config['FACEBOOK_APP_ID'], state=session['oauth_state'])
    token = facebook.fetch_token('https://graph.facebook.com/v11.0/oauth/access_token', authorization_response=request.url, client_secret=app.config['FACEBOOK_APP_SECRET'])
    user_data = facebook.get(FACEBOOK_API_URL + 'me?fields=id,name,email').json()
    return f"Добро пожаловать, {user_data['name']}!"

@app.route('/logout')
def logout():
    return "Вы успешно вышли."


if __name__ == '__main__':
    app.run(port=4042)

