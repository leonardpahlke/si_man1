import csv


def validate_input(inp):
    while inp.lower() != 'y' and inp.lower() != 'n':
        inp = input('Try again [Y/n]: \n>>> ')

    if inp.lower() == 'y':
        return True
    else:
        return False


peopleToAdd = []


def add_people(f_name, l_name, email, phone, gender):
    print('Processing your request...')
    person = {
        "FirstName": f_name,
        "LastName": l_name,
        "Email": email,
        "Phone": phone,
        "Gender": gender
    }
    peopleToAdd.append(person)


print("Welcome to this registration client CLI!")

inp = input("Would you like to add a person? [Y/n]")

while True:
    flag = validate_input(inp)
    if flag:
        f_name = input("First name: ")
        l_name = input("Last name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        gender = input("Gender: ")
        add_people(f_name, l_name, email, phone, gender)
        inp = input("Add another one? ")
    else:
        with open("../server_service/people.csv", "w", newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['FirstName', 'LastName', 'Email', 'Phone', 'Gender'])
            for p in peopleToAdd:
                writer.writerow([p['FirstName'], p['LastName'], p['Email'], p['Phone'], p['Gender']])
        break