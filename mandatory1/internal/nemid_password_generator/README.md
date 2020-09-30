# NemID Password Generator:
## Task
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