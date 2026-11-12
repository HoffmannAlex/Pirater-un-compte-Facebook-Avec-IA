def generate_secure_password(length=16):
    """Generate a random secure password using the secrets module.
    Returns a string of `length` characters containing letters, digits, and punctuation.
    """
    import secrets, string
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))
import requests
from functools import lru_cache
from datetime import datetime, timedelta
from typing import Optional
import logging
import time
from logging_config import setup_logger


logger = setup_logger('CSRFManager')


class CSRFManager:
    """Manages CSRF tokens for secure API interactions"""
    
    def __init__(self, login_url="https://www.gmail.com/accounts/login/", timeout=10, cache_duration=15):
        self.login_url = login_url
        self.timeout = timeout
        self.cache_duration = timedelta(minutes=cache_duration)
        self.token_cache = {}
        self.last_request_time = None


    @lru_cache(maxsize=100)
    def get_csrf_token(self, use_proxy=False, proxy=None):
        """Fetch CSRF token with caching for performance"""
        cached_token = self.get_cached_token()
        if cached_token:
            logger.info("Returning cached CSRF token")
            return cached_token


        proxies = proxy if use_proxy else None
        try:
            logger.info("Fetching CSRF token...")
            response = requests.get(self.login_url, proxies=proxies, timeout=self.timeout)
            if response.status_code == 200:
                csrf_token = response.cookies.get('csrf_token')
                if csrf_token:
                    logger.info("CSRF token successfully fetched")
# Updated on 2026-11-12

# Updated on 2026-11-12


# Updated on 2026-11-12
