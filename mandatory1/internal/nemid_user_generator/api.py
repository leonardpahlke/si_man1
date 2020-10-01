# library imports
from fastapi import FastAPI
from pydantic import BaseModel, Field
import re
import sys

# local package imports
from mandatory1.config.namings import API_DESCRIPTION
from mandatory1.config.deployment import ADDRESS, DOCS_ENDPOINT
from mandatory1.config.vars import NEM_ID_LENGTH, CPR_LENGTH
from mandatory1.pkg.api_documentation import Custom_openapi
from mandatory1.pkg.rnd_util import Random_with_N_digits


sys.path.append('../../../mandatory1')

app = FastAPI(docs_url=DOCS_ENDPOINT)

# Variables
PASS_LAST_DIGITS_CPR = 4
GENERATED_NUMBER_LENGTH = 5

PORT = "8088"

API_TITLE = "NemID User Generator"

# for validating an Email
EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


# API Type Models
class NemIdUserGenInfo(BaseModel):
    cpr: str = Field("", title="cpr", description="some 10 digit CPR")
    email: str = Field("", title="email", description="your email address")


class NemIdResponse(BaseModel):
    nemId: int = Field("", title="nemId", description="random_5_digit_number-Last_4_digits_of_cpr")
    statusCode: int = Field(200, title="status-code", description="http status-code")
    message: str = Field(200, title="message", description="response message")


# API Paths
@app.get("/", tags=["Ping"])
def read_root():
    return {API_TITLE + ", Documentation": ADDRESS + ":" + PORT + DOCS_ENDPOINT}


@app.post("/generate-nemID", response_model=NemIdResponse, name="Generate NemId code", tags=["NemId Code"])
def log(code_id_info: NemIdUserGenInfo):
    if (len(str(code_id_info.cpr)) == CPR_LENGTH) or (re.search(EMAIL_REGEX, code_id_info.email)):
        random_number = Random_with_N_digits(GENERATED_NUMBER_LENGTH)
        nem_id = int(str(random_number) + str(code_id_info.cpr[-PASS_LAST_DIGITS_CPR:]))
        return NemIdResponse(nemId=nem_id, statusCode=200, message="NemId created")
    else:
        # input invalid because (cpr != eleven digits) OR (email format invalid)
        return NemIdResponse(nemId=0, statusCode=403, message="Invalid input")


app.openapi = Custom_openapi(app, API_TITLE, API_DESCRIPTION, "1.0.0")

# local testing
# uvicorn api:app --reload --port 8088

# --host 127.0.0.1
