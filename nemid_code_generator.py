# library imports
from fastapi import FastAPI
from pydantic import BaseModel, Field
import sqlalchemy as db
import random

# local package imports
from config import ADDRESS, DOCS_ENDPOINT, NEM_ID_CODE_LENGTH, NEM_ID_LENGTH

# NEMID CODE GENERATOR
# 1. Will receive a POST request at http://localhost:8090/nemid-auth with JSON body
# {
#   "nemIdCode": "code of four digits",
#   "nemId": "generated 9 digit nemId"
# }
# 2. Check against the data from the database. If it matches this will return a JSON body with status code 200.
# Otherwise it will return a 403 (forbidden): {generatedCode": "random 6 digits code"}

app = FastAPI(docs_url=DOCS_ENDPOINT)

# Variables
PORT = "8090"

GENERATED_NUMBER_LENGTH = 6

API_TITLE = "NemId Code Generator"

DB_FILE_PATH = "sqlite:///NemID_ESB/nem_id_database.sqlite"
# Base = declarative_base()


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
            random_number = random_with_N_digits(GENERATED_NUMBER_LENGTH)
            return NemIdGeneratedCode(generatedCode=random_number, statusCode=200, message="NemId-code generated")
        else:
            # user provided invalid information
            return NemIdGeneratedCode(generatedCode=0, statusCode=403, message="NemId not found")


# Check against the data from the database
def checkNemIdInDB(code_id_info: NemIdCodeGenInfo) -> bool:
    # TODO: establish database connection to sqlite file
    engine = db.create_engine(DB_FILE_PATH)
    connection = engine.connect()
    metadata = db.MetaData()
    db_user_table = db.table('user', metadata, autoload=True, autoload_with=engine)

    # TODO: query database if nemId can be found

    # TODO: return result

    # user = db.session.query(EntityUser).filter(EntityUser.NemID == code_id_info.nemId).first()
    # return user & True  # TODO check if this returns correctly
    return True


class EntityUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    CPR = Column(String)
    NemID = Column(String)
    Password = Column(String)

    def __repr__(self):
        return "<User(CPR='%s', NemID='%s', Password='%s')>" % (self.CPR, self.NemID, self.Password)


def random_with_N_digits(n):
    return int("".join([str(random.randint(0, 9)) for _ in range(n)]))

# local testing
# uvicorn nemid_code_generator:app --reload --port 8090

# --host 127.0.0.1
