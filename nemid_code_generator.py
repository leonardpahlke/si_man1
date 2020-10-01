# library imports
from fastapi import FastAPI
from pydantic import BaseModel, Field

# local package imports
from config import ADDRESS, DOCS_ENDPOINT, API_DESCRIPTION, NEM_ID_CODE_LENGTH, NEM_ID_LENGTH
from pkg import Random_with_N_digits, Custom_openapi

app = FastAPI(docs_url=DOCS_ENDPOINT)

# Variables
PORT = "8090"

GENERATED_NUMBER_LENGTH = 6

API_TITLE = "NemId Code Generator"


# API Type Models
class NemIdCodeGenInfo(BaseModel):
    nemIdCode: str = Field("", title="nemIdCode", description="code of four digits")
    nemId: str = Field("", title="nemId", description="generated 9 digit nemId")


class NemIdGeneratedCode(BaseModel):
    generatedCode: int = Field("", title="generatedCode", description="random 6 digits code")
    statusCode: int = Field(200, title="status-code", description="http status-code")
    message: str = Field(200, title="message", description="response message")


# API Paths
@app.get("/", tags=["Ping"])
def read_root():
    return {API_TITLE + ", Documentation": ADDRESS + ":" + PORT + DOCS_ENDPOINT}


@app.post("/nemid-auth", response_model=NemIdGeneratedCode, name="Generate NemId code", tags=["NemId Code"])
def log(code_id_info: NemIdCodeGenInfo):
    if (len(str(code_id_info.nemIdCode)) != NEM_ID_CODE_LENGTH) or (len(str(code_id_info.nemId)) != NEM_ID_LENGTH):
        # input invalid because (nemIdCode != four digits) OR (nemId != 9 digits)
        return NemIdGeneratedCode(generatedCode=0, statusCode=403, message="Invalid input")
    else:
        if checkNemIdInDB(code_id_info):
            # user provided valid information
            random_number = Random_with_N_digits(GENERATED_NUMBER_LENGTH)
            return NemIdGeneratedCode(generatedCode=random_number, statusCode=200, message="NemId-code generated")
        else:
            # user provided invalid information
            return NemIdGeneratedCode(generatedCode=0, statusCode=403, message="NemId not found")


# Check against the data from the database
def checkNemIdInDB(code_id_info: NemIdCodeGenInfo) -> bool:
    # TODO check database
    return True


app.openapi = Custom_openapi(app, API_TITLE, API_DESCRIPTION, "1.0.0")

# local testing
# uvicorn api:app --reload --port 8090

# --host 127.0.0.1

if __name__ == "__main__":
    print("Hello")