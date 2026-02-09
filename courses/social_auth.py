from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from rest_framework import exceptions
import os

def verify_google_token(token):
    try:
        # Lấy Client ID từ environment hoặc settings
        client_id = os.getenv('GOOGLE_CLIENT_ID')
        
        # Xác thực token với Google (thêm clock_skew_in_seconds để fix lỗi lệch giờ giữa các server)
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id, clock_skew_in_seconds=10)

        # Kiểm tra issuer
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # ID token is valid. Get the user's Google ID from the decoded token.
        return idinfo
    except Exception as e:
        error_msg = str(e)
        print(f"Google token verification error: {error_msg}")
        return {"error": error_msg}
