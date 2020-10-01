# KEA System Integration - Mandatory Assignment 1
_Winter Semester 2020/2021_ 

_Author: Leonard Pahlke_


The purpose of this assignment is to showcase different scenarios and integration techniques in a way that contributes 
to the creation of a solution that incorporates file-based integration, shared databases as well as RPC (web services 
and RESTful APIs) integration patterns.

## System Diagram
![System Diagram](./assets/SI-Mandatory1-SystemDiagram%202020-09-30%20at%2011.02.48.png)

## Getting Started

1. **Install**
    1. install python3.8
    2. setup local environment run `source install.bash`
2. **Start API's**
    1. `uvicorn nemid_user_generator:app --reload --port 8088`
    2. `uvicorn nemid_password_generator:app --reload --port 8089`
    3. `uvicorn nemid_code_generator:app --reload --port 8090`
3. **Access API Documentations**
    1. [localhost:8088, NemId user generator](http://localhost:8088/docs)
    2. [localhost:8088, NemId password generator](http://localhost:8089/docs)
    3. [localhost:8088, NemId code generator](http://localhost:8090/docs)  

_execute scripts within the terminal from the project root folder. When using uvicorn the python virtual environment need to be activated_

## Mandatory 1 - Module descriptions

### NemID Password Generator
1. Will receive a POST request to http://localhost:8089/generate-password-nemID with body:
```json
{
"cpr": "cpr_number",
"nemId": "random_5_digit_number-Last_4_digits_of_cpr"
}
```
2. Will send a JSON response (status 200):
```json
{
"nemIdPassword": "first 2 digits of nemId and last 2 digits of the cpr"
}
```

### NemID Code Generator
1. Will receive a POST request at http://localhost:8090/nemid-auth with JSON body
```json
{
"nemIdCode": "code of four digits",
"nemId": "generated 9 digit nemId"
}
```
2. Check against the data from the database. If it matches this will return a JSON body with status code 200. Otherwise it will return a 403 (forbidden):
```json
{
"generatedCode": "random 6 digits code"
}
```

### NemID User Generator
1. Will receive a POST request to http://localhost:8088/generate-nemID with body:
```json
{
"cpr": "some 10 digit CPR",
"email": "some@email.com"
}
```
2. Will return a JSON response (status 201):
```json
{
"nemId": "random_5_digit_number-Last_4_digits_of_cpr"
}
```