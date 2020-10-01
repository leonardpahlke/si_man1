import json
import requests
import csv
import xml.etree.ElementTree as ElementTree

from pkg import Random_with_N_digits, PersonCsvConfig


# LEGACY CENTRAL SYSTEM
# 1. The system must read the people.csv file
# 2. For each person that is found in the file it will:
#     1. Generate a CPR similarly to how a normal CPR looks: ddMMyyy-[random-4-digits]
#     2. Build an xml body that contains the firstname, lastname and CPR number
#    <?xml version="1.0" ?>
#    <Person>
#      <FirstName>Jon</FirstName>
#      <LastName>Doe</LastName>
#      <CprNumber>1234567890</CprNumber>
#      <Email>dummy@example.com</Email>
#    </Person>
#     3. Send a POST request to http://localhost:8080/nemID with the XML as a body
#     4. The NemID system will return a JSON body: `{"nemID": "some 9 digit nemID"}`
#     5. An msgpack file will be created with the name [CPR]. msgpack which will contain f_name, l_name,
#     birth_date[DD-MM-YYYY], email, country, phone, address, CPR and NemID number.
#     > I suggest you make a JSON object and then serialize it.

CSV_FILE_NAME = "people.csv"
CSV_LOCATION = "Main_System/" + CSV_FILE_NAME

MSG_PACK_NAME = "CPR"

CPR_GENERATED_NUMBER_LENGTH = 4

ESB_SERVICE_ADDRESS = "http://localhost:8080"
ESB_SERVICE_API_NEMID_ENDPOINT = "/nemID"
REQUEST_HEADERS = {'Content-Type': 'text/xml', 'Accept': 'application/xml'}


# The system must read the people.csv file
def read_csv_file(csv_config: PersonCsvConfig):
    csv_persons = []
    with open(csv_config.csv_file_name, newline='') as csv_config.csv_location:
        persons = csv.reader(csv_config.csv_file_name, delimiter=csv_config.delimiter)
        for person in persons:
            print(', '.join(person))
            csv_persons.append({
                "LastName": person[csv_config.csv_lastname_position],
                "FirstName": person[csv_config.csv_firstname_position],
                "Email": person[csv_config.csv_email_position],
                "Phone": person[csv_config.csv_phone_position]
            })
    return csv_persons


# TODO check I can add here multiple persons as well
# Maybe split at serializing step
def add_person(person):
    lastname = person["LastName"]
    firstname = person["FirstName"]
    email = person["Email"]
    date_of_birth = person["DateOfBirth"]
    phone = person["Phone"]
    address = person["Address"]
    country = person["Country"]

    # Generate a CPR similarly to how a normal CPR looks: ddMMyyyy-[random-4-digits]
    cpr = "{}-{}".format(date_of_birth.replace("-", ""), Random_with_N_digits(CPR_GENERATED_NUMBER_LENGTH))

    # Build an xml body that contains the firstname, lastname and CPR number
    xml = build_xml(firstname, lastname, cpr, email)

    # Send a POST request to http://localhost:8080/nemID with the XML as a body
    response = requests.post(ESB_SERVICE_ADDRESS + ESB_SERVICE_API_NEMID_ENDPOINT, headers=REQUEST_HEADERS, data=xml)
    # 4. The NemID system will return a JSON body: `{"nemID": "some 9 digit nemID"}`
    json_response = json.loads(response.text)
    nem_id = json_response["nemID"]

    # An msgpack file will be created with the name [CPR]. msgpack which will contain f_name, l_name,
    # birth_date[DD-MM-YYYY], email, country, phone, address, CPR and NemID number.
    # I suggest you make a JSON object and then serialize it.
    msg_person_payload = {
        "f_name": firstname,
        "l_name": lastname,
        "birth_date": date_of_birth,
        "email": email,
        "phone": phone,
        "country": country,
        "address": address,
        "CPR": cpr,
        "NemID": nem_id
    }
    msg_person_payload_json = json.dumps(msg_person_payload)
    create_msg_pack(msg_person_payload_json)


# Build an xml body that contains the firstname, lastname and CPR number
# <?xml version="1.0" ?>
# <Person>
#     <FirstName>Jon</FirstName>
#     <LastName>Doe</LastName>
#     <CprNumber>1234567890</CprNumber>
#     <Email>dummy@example.com</Email>
# </Person>
def build_xml(firstname, lastname, cpr, email) -> str:
    # create xml 'Person' root
    p_person = ElementTree.Element('Person')
    # create xml children
    ElementTree.SubElement(p_person, 'FirstName', firstname)
    ElementTree.SubElement(p_person, 'LastName', lastname)
    ElementTree.SubElement(p_person, 'CprNumber', cpr)
    ElementTree.SubElement(p_person, 'Email', email)
    # return xml as string
    return ElementTree.tostring(p_person, encoding='utf8', method='xml')


# serialize
def create_msg_pack(msg_person_payload_json):
    # TODO
    return msg_person_payload_json


if __name__ == "__main__":
    # TODO
    pass
