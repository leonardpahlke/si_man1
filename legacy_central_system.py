import json
import requests
import csv
import xml.etree.ElementTree as ElementTree
import msgpack
import random

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

CPR_GENERATED_NUMBER_LENGTH = 4
LOGGING = False

ESB_SERVICE_ADDRESS = "http://localhost:8080"
ESB_SERVICE_API_NEMID_ENDPOINT = "/nemID"
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

    def setPersonDetails(self, person_information_list) -> bool:
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

    def setNemId(self, nem_id):
        self.nemId = nem_id

    def setCPR(self, cpr):
        self.cpr = cpr

    def transformPersonToDICT(self) -> json:
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
        return str(self.transformPersonToDICT())


# The system must read the people.csv file
def read_csv_file(csv_location, delimiter=","):
    csv_persons = []
    with open(csv_location, newline='') as csv_file:
        persons_reader = csv.reader(csv_file, delimiter=delimiter)
        next(persons_reader)  # skip first element
        for person in persons_reader:
            person_wrapper = CSVUser()
            if person_wrapper.setPersonDetails(person):
                csv_persons.append(person_wrapper)
    return csv_persons


# TODO check I can add here multiple persons as well
# Maybe split at serializing step
def add_person(person_wrapper):
    if LOGGING:
        print("ADD Person:", person_wrapper)

    # Generate a CPR similarly to how a normal CPR looks: ddMMyyyy-[random-4-digits]
    cpr = "{}-{}".format(person_wrapper.dateOfBirth.replace("-", ""), random_with_N_digits(CPR_GENERATED_NUMBER_LENGTH))
    person_wrapper.setCPR(cpr)

    if LOGGING:
        print("CPR created:", cpr)

    # Build an xml body that contains the firstname, lastname and CPR number
    xml = build_xml(person_wrapper.firstname, person_wrapper.lastname, person_wrapper.cpr, person_wrapper.email)
    if LOGGING:
        print("XML created:", xml)

    # Send a POST request to http://localhost:8080/nemID with the XML as a body
    response = requests.post(ESB_SERVICE_ADDRESS + ESB_SERVICE_API_NEMID_ENDPOINT, headers=REQUEST_HEADERS, data=xml)
    # 4. The NemID system will return a JSON body: `{"nemID": "some 9 digit nemID"}`
    json_response = json.loads(response.text)
    nem_id = json_response["nemID"]
    person_wrapper.setNemId(nem_id)
    if LOGGING:
        print("Person Information updated:", person_wrapper)

    # An msgpack_data file will be created with the name [CPR]. msgpack_data which will contain f_name, l_name,
    # birth_date[DD-MM-YYYY], email, country, phone, address, CPR and NemID number.
    # I suggest you make a JSON object and then serialize it.

    msg_person_payload_json = json.loads(person_wrapper.transformPersonToDICT())
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
    print(firstname, lastname, cpr, email)
    p_person = ElementTree.Element('Person')
    # create and set xml children
    ElementTree.SubElement(p_person, 'FirstName').text = firstname
    ElementTree.SubElement(p_person, 'LastName').text = lastname
    ElementTree.SubElement(p_person, 'CprNumber').text = cpr
    ElementTree.SubElement(p_person, 'Email').text = email
    # return xml as string
    return ElementTree.tostring(p_person, encoding='utf8', method='xml')


# serialize a person dictionary
def create_msg_pack(msg_person_payload_json):
    # Write msgpack_data file (named: "<email>cpr.msgpack" to have a unique file for a each person)
    with open(MSG_PACK_LOCATION + msg_person_payload_json["email"] + "cpr.msgpack", "wb") as outfile:
        packed = msgpack.packb(msg_person_payload_json)
        outfile.write(packed)


def ReadCsvAndCreateMsgpack():
    list_person_dict = read_csv_file(CSV_LOCATION)
    for person in list_person_dict:
        add_person(person)


def random_with_N_digits(n):
    return int("".join([str(random.randint(0, 9)) for _ in range(n)]))


if __name__ == "__main__":
    mode = input("Create persons from csv [y/n]: ")
    if mode == "y":
        LOGGING = True  # TODO
        ReadCsvAndCreateMsgpack()
    else:
        print("exit legacy system...")
