#

## Task
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