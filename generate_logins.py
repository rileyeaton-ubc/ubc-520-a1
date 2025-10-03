import random
import string
from faker import Faker
from tqdm import tqdm

fake = Faker()

DATA_PATH = "./data/logins.txt"

def generate_login():
    strategy = random.choice(['username', 'firstname_numbers', 'lastname_numbers',
                             'firstname_lastname', 'email_prefix', 'random_letters'])

    if strategy == 'username':
        login = fake.user_name()
    elif strategy == 'firstname_numbers':
        login = fake.first_name().lower() + ''.join(random.choices(string.digits, k=random.randint(1, 4)))
    elif strategy == 'lastname_numbers':
        login = fake.last_name().lower() + ''.join(random.choices(string.digits, k=random.randint(1, 4)))
    elif strategy == 'firstname_lastname':
        login = fake.first_name().lower() + fake.last_name().lower()
    elif strategy == 'email_prefix':
        login = fake.email().split('@')[0]
    else:
        length = random.randint(5, 12)
        login = ''.join(random.choices(string.ascii_lowercase, k=length-2))
        login += ''.join(random.choices(string.digits, k=2))

    return login

def generate_unique_logins(count, output_file=DATA_PATH):
    logins = set()
    attempts = count * 2

    for _ in tqdm(range(attempts), desc='Generating logins'):
        logins.add(generate_login())
        if len(logins) >= count:
            break

    with open(output_file, 'w') as f:
        for login in tqdm(sorted(logins), desc='Writing to file'):
            f.write(login + '\n')

    print(f'Generated {len(logins)} unique logins to {output_file}')

if __name__ == '__main__':
    generate_unique_logins(10000000, DATA_PATH)
