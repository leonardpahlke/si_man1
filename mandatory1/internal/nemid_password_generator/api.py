# library imports
from fastapi import FastAPI
from pydantic import BaseModel, Field

# local package imports
from mandatory1.config.namings import API_DESCRIPTION
from mandatory1.config.deployment import ADDRESS, DOCS_ENDPOINT
from mandatory1.config.vars import NEM_ID_LENGTH, CPR_LENGTH
from mandatory1.pkg.api_documentation import Custom_openapi

app = FastAPI(docs_url=DOCS_ENDPOINT)

# Variables
PASS_FIRST_DIGITS_NEMID = 2
PASS_LAST_DIGITS_CPR = 2

PORT = "8089"

API_TITLE = "NemId Password Generator"


# API Type Models
class NemIdPasswordGenInfo(BaseModel):
    cpr: str = Field("", title="cpr", description="cpr_number")
    nemId: str = Field("", title="nemId", description="random_5_digit_number-Last_4_digits_of_cpr")


class NemIdPassword(BaseModel):
    nemIdPassword: int = Field("", title="nemIdPassword", description="first 2 digits of nemId and last 2 digits of the cpr")
    statusCode: int = Field(200, title="status-code", description="http status-code")
    message: str = Field(200, title="message", description="response message")


# API Paths
@app.get("/", tags=["Ping"])
def read_root():
    return {API_TITLE + ", Documentation": ADDRESS + ":" + PORT + DOCS_ENDPOINT}


@app.post("/generate-password-nemID", response_model=NemIdPassword, name="Generate NemId code", tags=["NemId Code"])
def log(code_id_info: NemIdPasswordGenInfo):
    if (len(str(code_id_info.cpr)) != CPR_LENGTH) or (len(str(code_id_info.nemId)) != NEM_ID_LENGTH):
        # input invalid because (cpr != eleven digits) OR (nemId != 9 digits)
        return NemIdPassword(nemIdPassword=0, statusCode=403, message="Invalid input")
    else:
        password = int(str(code_id_info.cpr[:PASS_FIRST_DIGITS_NEMID]) + str(code_id_info.cpr[-PASS_LAST_DIGITS_CPR:]))
        return NemIdPassword(nemIdPassword=password, statusCode=200, message="NemId-password created")


app.openapi = Custom_openapi(app, API_TITLE, API_DESCRIPTION, "1.0.0")

# local testing
# uvicorn api:app --reload --port 8089

# --host 127.0.0.1
