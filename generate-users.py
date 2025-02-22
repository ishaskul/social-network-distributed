import csv
import random
import string
import sys

def dump_data(data, filename):
    # Write data to a CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'password', 'firstname', 'lastname'])  # Header row
        writer.writerows(data)

def generate_password():
    password_length = random.randint(8, 12)
    password_characters = string.ascii_letters  # + string.digits # + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(password_length))

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <number_of_entries> <output_filename>")
        sys.exit(1)

    try:
        num_entries = int(sys.argv[1])
    except ValueError:
        print("The number of entries must be an integer.")
        sys.exit(1)

    filename = sys.argv[2]

    # Generate random data for the CSV file
    data = []
    for i in range(num_entries):
        username = ''.join(random.choices(string.ascii_lowercase, k=5))
        password = generate_password()
        first_name = ''.join(random.choices(string.ascii_uppercase, k=5))
        last_name = ''.join(random.choices(string.ascii_uppercase, k=5))

        data.append([username, password, first_name, last_name])

    # Dump all data into a single CSV file
    dump_data(data, filename)

if __name__ == "__main__":
    main()