from random import randint
from fastapi.openapi.utils import get_openapi


# custom API documentation
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


def Random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)