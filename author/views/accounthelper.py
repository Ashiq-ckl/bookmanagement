from django.urls import reverse
from django.http import HttpRequest

from oauth2_provider.views.mixins import OAuthLibMixin
from oauth2_provider.models import get_access_token_model, get_refresh_token_model
from oauth2_provider.signals import app_authorized
from author.costantvariables import AUTH_CLIENT_ID,AUTH_CLIENT_SECRET
import json

class AdminOAuth2Token( OAuthLibMixin ):
    def __init__(self) -> None:
        self.client_id = AUTH_CLIENT_ID
        self.client_secret = AUTH_CLIENT_SECRET

    def generate_oauth_token(self, username, password):
        request_ = HttpRequest()
        request_.method = "POST"
        request_.POST = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        url, headers, body, token_status = self.create_token_response( request_ )
        body_ = json.loads( body )
        access_token = body_.get("access_token", None)        
        if access_token is not None:
            token = get_access_token_model().objects.get( token=access_token )
            app_authorized.send( sender=self, request=request_, token=token )
            records = {
                "result":'success',
                "token": body_,
            }
            return records
        else:
            return {"result": "failure", "errors": body_}
    
    