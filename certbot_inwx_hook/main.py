#!/usr/bin/env python3

import os
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
        style="{", format="certbot_inwx_hook:{levelname}: {message}")

from .constants import CERTBOT_DOMAIN_ENV, CERTBOT_VALIDATION_ENV
from .inwx_challenge import InwxChallenge

def deploy():
    """Deploys INWX challenge"""
    domain = os.environ.get(CERTBOT_DOMAIN_ENV)
    validation = os.environ.get(CERTBOT_VALIDATION_ENV)
    InwxChallenge(domain, validation).deploy_challenge()

def cleanup():
    """Cleans INWX challenge"""
    domain = os.environ.get(CERTBOT_DOMAIN_ENV)
    validation = os.environ.get(CERTBOT_VALIDATION_ENV)
    InwxChallenge(domain, validation).clean_challenge()
