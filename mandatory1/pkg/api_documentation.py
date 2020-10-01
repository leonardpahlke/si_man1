# add api description
from fastapi.openapi.utils import get_openapi


def Custom_openapi(app, api_title, api_description, version):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=api_title,
        version=version,
        description=api_description,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
