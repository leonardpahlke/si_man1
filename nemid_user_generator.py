# library imports
from fastapi import FastAPI
from pydantic import BaseModel, Field
import re
import random

# local package imports
from config import ADDRESS, DOCS_ENDPOINT, CPR_LENGTH

# NEMID USER GENERATOR
# 1. Will receive a POST request to http://localhost:8088/generate-nemID with body:
# {
#   "cpr": "some 10 digit CPR",
#   "email": "some@email.com"
# }
# 2. Will return a JSON response (status 201): { "nemId": "random_5_digit_number-Last_4_digits_of_cpr" }

app = FastAPI(docs_url=DOCS_ENDPOINT)

# Variables
PASS_LAST_DIGITS_CPR = 4
GENERATED_NUMBER_LENGTH = 5

PORT = "8088"

API_TITLE = "NemID User Generator"

# for validating the Email format
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


@app.post("/generate-nemId", response_model=NemIdResponse, name="Generate NemId code", tags=["NemId Code"])
def log(code_id_info: NemIdUserGenInfo):
    print(re.search(EMAIL_REGEX, code_id_info.email) is not None)
    if (len(str(code_id_info.cpr)) == CPR_LENGTH) and (re.search(EMAIL_REGEX, code_id_info.email) is not None):
        nem_id = int(str(random_with_n_digits(GENERATED_NUMBER_LENGTH)) + str(code_id_info.cpr[-PASS_LAST_DIGITS_CPR:]))
        return NemIdResponse(nemId=nem_id, statusCode=200, message="NemId created")
    else:
        # input invalid because (cpr != eleven digits) OR (email format invalid)
        return NemIdResponse(nemId=0, statusCode=403, message="Invalid input")


def random_with_n_digits(n):
    return int("".join([str(random.randint(0, 9)) for _ in range(n)]))
# local testing
# uvicorn nemid_user_generator:app --reload --port 8088

# --host 127.0.0.1
