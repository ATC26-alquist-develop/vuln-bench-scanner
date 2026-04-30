```python
import http.cookies
import secrets
import hashlib
from typing import Dict
from datetime import datetime, timedelta

class SecureCookieManager:
    def __init__(self):
        # Generate a secure secret key for signing cookies
        self._secret_key = secrets.token_bytes(32)
        self._cookie_settings = {
            'max_age': 3600 * 24 * 30,  # 30 days
            'secure': True,
            'httponly': True,
            'samesite': 'Strict'
        }

    def create_visit_cookie(self, user_id: str) -> str:
        """
        Creates a secure cookie to track user visits.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            A string containing the cookie value
        """
        # Validate user_id to prevent injection
        if not user_id or not isinstance(user_id, str):
            raise ValueError("Invalid user ID")

        # Create a timestamp for the cookie
        timestamp = datetime.utcnow().isoformat()

        # Create cookie value with user ID and timestamp
        cookie_value = f"{user_id}:{timestamp}"

        # Create and sign the cookie
        cookie = http.cookies.SimpleCookie(
            cookie_value,
            max_age=self._cookie_settings['max_age'],
            secure=self._cookie_settings['secure'],
            httponly=self._cookie_settings['httponly'],
            samesite=self._cookie_settings['samesite']
        )

        # Sign the cookie with HMAC-SHA256
        signed_value = self._sign_cookie(cookie.value)

        # Set the cookie and return the value
        cookie['signed'] = True
        cookie['path'] = '/'
        cookie['domain'] = '.example.com'  # Set appropriate domain
        return cookie.output(header='', sep='; ')

    def _sign_cookie(self, value: str) -> str:
        """
        Signs the cookie value using HMAC-SHA256.
        
        Args:
            value: The cookie value to sign
            
        Returns:
            The signed cookie value
        """
        # Create a signature using HMAC-SHA256
        signature = hashlib.sha256(
            f"{value}:{self._secret_key}".encode('utf-8')
        ).hexdigest()
        
        # Return the signed value
        return f"{value}:{signature}"

    def validate_and_read_cookie(self, cookie_value: str) -> Dict[str, str]:
        """
        Validates and reads a cookie value.
        
        Args:
            cookie_value: The cookie value to validate
            
        Returns:
            A dictionary containing user ID and timestamp if valid
        """
        try:
            # Split the signed value into value and signature
            parts = cookie_value.split(':')
            if len(parts) != 2:
                raise ValueError("Invalid cookie format")

            value, signature = parts

            # Verify the signature
            expected_signature = hashlib.sha256(
                f"{value}:{self._secret_key}".encode('utf-8')
            ).hexdigest()

            if signature != expected_signature:
                raise ValueError("Invalid cookie signature")

            # Parse the value
            user_id, timestamp = value.split(':')

            # Validate user ID
            if not user_id or not isinstance(user_id, str):
                raise ValueError("Invalid user ID")

            # Validate timestamp
            try:
                cookie_time = datetime.fromisoformat(timestamp)
            except ValueError:
                raise ValueError("Invalid timestamp")

            # Check if cookie has expired
            if datetime.utcnow() > cookie_time:
                raise ValueError("Cookie has expired")

            return {'user_id': user_id, 'timestamp': timestamp}

        except Exception as e:
            # Log the error here if needed
            raise ValueError(f"Cookie validation failed: {str(e)}")

    def clear_cookie(self) ->