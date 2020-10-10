# library imports
from fastapi import FastAPI
from pydantic import BaseModel, Field

# local package imports
from config import ADDRESS, DOCS_ENDPOINT, NEM_ID_LENGTH, CPR_LENGTH

# NEMID PASSWORD GENERATOR
# 1. Will receive a POST request to http://localhost:8089/generate-password-nemID with body:
# {
#   "cpr": "cpr_number",
#   "nemId": "random_5_digit_number-Last_4_digits_of_cpr"
# }
# 2. Will send a JSON response (status 200): { "nemIdPassword": "first 2 digits of nemId and last 2 digits of the cpr" }

app = FastAPI(docs_url=DOCS_ENDPOINT)

# Variables
PASS_FIRST_DIGITS_NEMID = 2
PASS_LAST_DIGITS_CPR = 2

NEMID_LAST_DIGITS_CPR = 4

PORT = "8089"

API_TITLE = "NemId Password Generator"


# API Type Models
class NemIdPasswordGenInfo(BaseModel):
    cpr: str = Field("", title="cpr", description="cpr_number")
    nemId: str = Field("", title="nemId", description="random_5_digit_number-Last_4_digits_of_cpr")


class NemIdPassword(BaseModel):
    nemIdPassword: int = Field("", title="nemIdPassword",
                               description="first 2 digits of nemId and last 2 digits of the cpr")
    statusCode: int = Field(200, title="status-code", description="http status-code")
    message: str = Field(200, title="message", description="response message")


# API Paths
@app.get("/", tags=["Ping"])
def read_root():
    return {API_TITLE + ", Documentation": ADDRESS + ":" + PORT + DOCS_ENDPOINT}


@app.post("/generate-password-nemID", response_model=NemIdPassword, name="Generate NemId code", tags=["NemId Code"])
def log(code_id_info: NemIdPasswordGenInfo):
    print("generate-password-nemID")
    # (CPR, NEMID length is correct) AND (check if NEMID has Last_4_digits_of_cpr)
    if ((len(str(code_id_info.cpr)) != CPR_LENGTH) or (len(str(code_id_info.nemId)) != NEM_ID_LENGTH)) or \
            (code_id_info.cpr[-NEMID_LAST_DIGITS_CPR:] != code_id_info.nemId[-NEMID_LAST_DIGITS_CPR:]):
        # input invalid because (cpr != eleven digits) OR (nemId != 9 digits) OR NEMID hasn't Last_4_digits_of_cpr
        print("err")
        return NemIdPassword(nemIdPassword=0, statusCode=403, message="Invalid input")
    else:
        password = int(str(code_id_info.cpr[:PASS_FIRST_DIGITS_NEMID]) + str(code_id_info.cpr[-PASS_LAST_DIGITS_CPR:]))
        print("generated password:", password)
        return NemIdPassword(nemIdPassword=password, statusCode=200, message="NemId-password created")

# local testing
# uvicorn nemid_password_generator:app --reload --port 8089

# --host 127.0.0.1
