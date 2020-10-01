import json
from datetime import datetime
import requests
import csv
import xml.etree.ElementTree as ElementTree

from pkg import Random_with_N_digits, PersonCsvConfig

CSV_FILE_NAME = "people.csv"
CSV_LOCATION = "../server_service/" + CSV_FILE_NAME

MSG_PACK_NAME = "CPR"

CPR_GENERATED_NUMBER_LENGTH = 4
COUNTRY = "Denmark"
NONE_ADDRESS = "unknown"

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


def add_person(person):
    lastname = person["LastName"]
    firstname = person["FirstName"]
    email = person["Email"]
    phone = person["Phone"]
    # gender = person["Gender"]  # this information is at the moment not getting processed and therefore commented out

    # Generate a CPR similarly to how a normal CPR looks: ddMMyyyy-[random-4-digits]
    birthday_time = datetime.now()
    birthday = birthday_time.strftime("%d%m%Y")  # birthday attr not given therefore current date will be assigned !!!
    cpr = generate_cpr(birthday)

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
        "birth_date": birthday_time.strftime("%d-%m-%Y"),
        "email": email,
        "phone": phone,
        "country": COUNTRY,
        "address": NONE_ADDRESS,  # address attr not given therefore none address will be assigned !!!
        "CPR": cpr,
        "NemID": nem_id
    }
    msg_person_payload_json = json.dumps(msg_person_payload)
    create_msg_pack(msg_person_payload_json)


def generate_cpr(birthday):
    random_number = Random_with_N_digits(CPR_GENERATED_NUMBER_LENGTH)
    return str(birthday) + "-" + str(random_number)


# Build an xml body that contains the firstname, lastname and CPR number
# <?xml version="1.0" ?>
# <Person>
#     <FirstName>Jon</FirstName>
#     <LastName>Doe</LastName>
#     <CprNumber>1234567890</CprNumber>
#     <Email>dummy@example.com</Email>
# </Person>
def build_xml(firstname, lastname, cpr, email):
    # create xml 'Person' root
    p_person = ElementTree.Element('Person')
    # create xml children
    ElementTree.SubElement(p_person, 'FirstName', firstname)
    ElementTree.SubElement(p_person, 'LastName', lastname)
    ElementTree.SubElement(p_person, 'CprNumber', cpr)
    ElementTree.SubElement(p_person, 'Email', email)
    # return xml as string
    return ElementTree.tostring(p_person)


def create_msg_pack(msg_person_payload_json):
    return msg_person_payload_json


if __name__ == "__main__":
    pass
