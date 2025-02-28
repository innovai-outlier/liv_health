import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

AUTH_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "auth_config.yaml")

def login_user():
    """ Gerencia autenticação do usuário via arquivo auth_config.yaml """
    with open(AUTH_CONFIG_FILE, "r") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )

    return authenticator.login("Login", "main")
