from random import randint
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class NemIdCodeGenInfo(BaseModel):
    nemIdCode: str = Field("", title="nemIdCode", description="code of four digits")
    nemId: str = Field("", title="nemId", description="generated 9 digit nemId")


class NemIdGeneratedCode(BaseModel):
    generatedCode: int = Field("", title="generatedCode", description="random 6 digits code")
    statusCode: int = Field(200, title="status-code", description="http status-code")


ADDRESS = "http://127.0.0.1"
PORT = "8090"

GeneratedNumberLength = 6
NemIdCodeLength = 4
NemIdLength = 9


@app.get("/", tags=["Ping"])
def read_root():
    return {"NemId Code Generator, Documentation": ADDRESS + ":" + PORT + "/docs"}


@app.post("/nemid-auth", response_model=NemIdGeneratedCode, name="Generate NemId code", tags=["NemId Code"])
def log(code_id_info: NemIdCodeGenInfo):
    if checkNemIdInDB(code_id_info):
        # user provided valid information
        random_number = random_with_N_digits(GeneratedNumberLength)
        return NemIdGeneratedCode(generatedCode=random_number, statusCode=200)
    else:
        # user provided invalid information
        return NemIdGeneratedCode(generatedCode=0, statusCode=403)


# add api description
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="NemID Code Generator API",
        version="1.0.0",
        description="This is Part of the KEA System Integration Mandatory Assignment 1 - by Leonard Pahlke",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Check against the data from the database
def checkNemIdInDB(code_id_info: NemIdCodeGenInfo) -> bool:
    if (len(str(code_id_info.nemIdCode)) != NemIdCodeLength) or (len(str(code_id_info.nemId)) != NemIdLength):
        # input invalid because (nemIdCode != code of four digits) OR (nemId != 9 digit nemId)
        return False
    # TODO check database
    return True


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


app.openapi = custom_openapi

# local testing
# uvicorn api:app --reload --port 8090

# --host 127.0.0.1 (redundant)
