import logging

from fastapi import FastAPI, Request


def logging_middleware(app: FastAPI):
    @app.middleware('http')
    async def dispatch(request: Request, call_next):
        logger = logging.getLogger('fast_api_service')
        request_id = request.headers.get('X-Request-Id')
        logger.info(
            'logging',
            extra={
                'request_url': request.url,
                'method': request.method,
                'request_id': request_id,
            },
        )

        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(e, extra={'request_id': request_id})
            raise e

        return response
