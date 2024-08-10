import csv
import random
import string

def dump_data(data, filename):
    # Write data to a CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'password', 'firstname', 'email'])  # Header row
        writer.writerows(data)

def generate_password():
    password_length = random.randint(8, 12)
    password_characters = string.ascii_letters  # + string.digits # + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(password_length))

# Generate random data for the CSV file
data = []
for i in range(10000):
    username = ''.join(random.choices(string.ascii_lowercase, k=5))
    password = generate_password()
    first_name = ''.join(random.choices(string.ascii_uppercase, k=5))
    email = f"user{i}@vu.nl"

    data.append([username, password, first_name, email])

# Dump all data into a single CSV file
dump_data(data, 'all_users.csv')

print("CSV file 'all_users.csv' created successfully with 10,000 random users.")