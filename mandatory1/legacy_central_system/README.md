# Legacy Central System

## Task
1. The system must read the people.csv file
2. For each person that is found in the file it will:
    1. Generate a CPR similarly to how a normal CPR looks: ddMMyyy-[random-4-digits] 
    2. Build an xml body that contains the firstname, lastname and CPR number
   ```XML
   <?xml version="1.0" ?>
   <Person>
     <FirstName>Jon</FirstName>
     <LastName>Doe</LastName>
     <CprNumber>1234567890</CprNumber>
     <Email>dummy@example.com</Email>
   </Person>
   ```
    3. Send a POST request to http://localhost:8080/nemID with the XML as a body 
    4. The NemID system will return a JSON body:
   `{"nemID": "some 9 digit nemID"}`
    5. An msgpack file will be created with the name [CPR]. msgpack which will contain f_name, l_name, birth_date[DD-MM-YYYY], email, country, phone, address, CPR and NemID number. 
    I suggest you make a JSON object and then serialize it.