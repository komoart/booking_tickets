import logging

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.utils import BadDsn

from core.config import settings


def init_sentry():
    try:
        sentry_sdk.init(dsn=settings.logging.SENTRY_DSN, integrations=[FastApiIntegration()])
    except BadDsn:
        logger = logging.getLogger('fast_api_service')
        logger.warning('Start without Sentry!')
