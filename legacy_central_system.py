import json
import requests
import csv
import xml.etree.ElementTree as ElementTree
import msgpack
import random
from io import BytesIO

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
#     5. An msgpack_data file will be created with the name [CPR]. msgpack_data which will contain f_name, l_name,
#     birth_date[DD-MM-YYYY], email, country, phone, address, CPR and NemID number.
#     > I suggest you make a JSON object and then serialize it.

CSV_LOCATION = "Main_System/people.csv"

MSG_PACK_LOCATION = "msgpack_data/"

ESB_SERVICE_ADDRESS = "http://localhost:8080"
ESB_SERVICE_NEMID_ENDPOINT = "nemID"

CPR_GENERATED_NUMBER_LENGTH = 4
LOGGING = False

REQUEST_HEADERS = {'Content-Type': 'text/xml', 'Accept': 'application/xml'}


class CSVUser:
    # FirstName,LastName,Email,DateOfBirth,Phone,Address,Country
    firstname: str = ""
    lastname: str = ""
    email: str = ""
    dateOfBirth: str = ""
    phone: str = ""
    address: str = ""
    country: str = ""
    nemId: str = ""
    cpr: str = ""

    def set_person_details(self, person_information_list) -> bool:
        if len(person_information_list) != 7:
            return False
        self.firstname = person_information_list[0]
        self.lastname = person_information_list[1]
        self.email = person_information_list[2]
        self.dateOfBirth = person_information_list[3]
        self.phone = person_information_list[4]
        self.address = person_information_list[5]
        self.country = person_information_list[6]
        return True

    def set_nem_id(self, nem_id):
        self.nemId = nem_id

    def set_cpr(self, cpr):
        self.cpr = cpr

    def transform_person_to_dict(self) -> json:
        return {
            "f_name": self.firstname,
            "l_name": self.lastname,
            "birth_date": self.dateOfBirth,
            "email": self.email,
            "country": self.country,
            "phone": self.phone,
            "address": self.address,
            "CPR": self.cpr,
            "NemID": self.nemId,
        }

    def __str__(self):
        return str(self.transform_person_to_dict())


# The system must read the people.csv file
def read_csv_file(csv_location, delimiter=","):
    csv_persons = []
    with open(csv_location, newline='') as csv_file:
        persons_reader = csv.reader(csv_file, delimiter=delimiter)
        next(persons_reader)  # skip first element
        for person in persons_reader:
            person_wrapper = CSVUser()
            if person_wrapper.set_person_details(person):
                csv_persons.append(person_wrapper)
    return csv_persons


# Maybe split at serializing step
def add_person(person_wrapper):
    if LOGGING:
        print("ADD Person:", person_wrapper)

    # Generate a CPR similarly to how a normal CPR looks: ddMMyyyy-[random-4-digits]
    cpr = "{}-{}".format(person_wrapper.dateOfBirth.replace("-", ""), random_with_n_digits(CPR_GENERATED_NUMBER_LENGTH))
    person_wrapper.set_cpr(cpr)

    if LOGGING:
        print("CPR created:", cpr)

    # Build an xml body that contains the firstname, lastname and CPR number
    xml = build_xml(person_wrapper.firstname, person_wrapper.lastname, person_wrapper.cpr, person_wrapper.email)

    # Send a POST request to http://localhost:8080/nemID with the XML as a body
    esb_service_nemid_endpoint = "{}/{}".format(ESB_SERVICE_ADDRESS, ESB_SERVICE_NEMID_ENDPOINT)
    if LOGGING:
        print("XML body created.. send request to: {}".format(esb_service_nemid_endpoint))
    response = requests.post(esb_service_nemid_endpoint, headers=REQUEST_HEADERS, data=xml)
    # 4. The NemID system will return a JSON body: `{"nemID": "some 9 digit nemID"}`
    json_response = json.loads(response.text)
    nem_id = json_response["nemID"]
    person_wrapper.set_nem_id(nem_id)
    if LOGGING:
        print("Person Information updated:", person_wrapper, ", response localhost/nemID:", json_response)

    # An msgpack_data file will be created with the name [CPR]. msgpack_data which will contain f_name, l_name,
    # birth_date[DD-MM-YYYY], email, country, phone, address, CPR and NemID number.
    # I suggest you make a JSON object and then serialize it.

    person_json_str = json.dumps(person_wrapper.transform_person_to_dict())
    create_msg_pack(person_json_str, person_wrapper.lastname)


# Build an xml body that contains the firstname, lastname and CPR number
# <?xml version="1.0" ?>
# <Person>
#     <FirstName>Jon</FirstName>
#     <LastName>Doe</LastName>
#     <CprNumber>1234567890</CprNumber>
#     <Email>dummy@example.com</Email>
# </Person>
def build_xml(firstname, lastname, cpr, email) -> bytes:
    # create xml 'Person' root
    print(firstname, lastname, cpr, email)
    p_person = ElementTree.Element('Person')
    # create and set xml children
    ElementTree.SubElement(p_person, 'FirstName').text = firstname
    ElementTree.SubElement(p_person, 'LastName').text = lastname
    ElementTree.SubElement(p_person, 'CprNumber').text = cpr
    ElementTree.SubElement(p_person, 'Email').text = email
    # return xml as string
    return ElementTree.tostring(p_person)


# serialize a person dictionary
def create_msg_pack(person_json_str, lastname):
    # Write msgpack_data file (named: "<lastname>cpr.msgpack" to have a unique file for a each person)
    file_path = "{}{}{}.msgpack".format(MSG_PACK_LOCATION, lastname, "Cpr")
    with open(file_path, "wb") as msgpack_file:
        packed = msgpack.packb(person_json_str)
        msgpack_file.write(packed)


def read_csv_and_create_msgpack():
    list_person_dict = read_csv_file(CSV_LOCATION)
    for person in list_person_dict:
        add_person(person)


def random_with_n_digits(n):
    return int("".join([str(random.randint(0, 9)) for _ in range(n)]))


if __name__ == "__main__":
    mode = input("Create persons from csv [y/n]: ")
    if mode.lower() == "y":
        logging = input("Log to console [y/n]: ")
        LOGGING = logging.lower() == "y"
        read_csv_and_create_msgpack()
    else:
        print("exit legacy system...")
