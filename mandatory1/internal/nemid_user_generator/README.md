# NemID User Generator

## Task
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