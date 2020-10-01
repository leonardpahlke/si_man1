from fastapi.openapi.utils import get_openapi
import random


def Random_with_N_digits(n):
    return int("".join([str(random.randint(0, 9)) for _ in range(n)]))


class PersonCsvConfig:
    delimiter: str
    csv_file_name: str
    csv_location: str
    # positions where the attribute is located after splitting a row into an array
    csv_firstname_position: int
    csv_lastname_position: int
    csv_email_position: int
    csv_phone_position: int
    csv_gender_position: int

    def __init__(self, csv_file_name, csv_location, delimiter=",", csv_firstname_position=0, csv_lastname_position=1,
                 csv_email_position=2, csv_phone_position=3, csv_gender_position=4):
        self.csv_file_name = csv_file_name
        self.csv_location = csv_location
        self.delimiter = delimiter
        self.csv_firstname_position = csv_firstname_position
        self.csv_lastname_position = csv_lastname_position
        self.csv_email_position = csv_email_position
        self.csv_phone_position = csv_phone_position
        self.csv_gender_position = csv_gender_position
