import random
import string
from faker import Faker
from tqdm import tqdm

# Initialize Faker for generating realistic names/usernames
fake = Faker()

DATA_PATH = "./data/logins.txt"

def generate_login():
    """
    Input: None
    Output: str - A randomly generated login name
    Generates a login using one of six different strategies for variety.
    """
    # Randomly select a generation strategy
    strategy = random.choice(['username', 'firstname_numbers', 'lastname_numbers',
                             'firstname_lastname', 'email_prefix', 'random_letters'])

    if strategy == 'username':
        login = fake.user_name()
    elif strategy == 'firstname_numbers':
        # Firstname with 1-4 random digits
        login = fake.first_name().lower() + ''.join(random.choices(string.digits, k=random.randint(1, 4)))
    elif strategy == 'lastname_numbers':
        # Lastname with 1-4 random digits
        login = fake.last_name().lower() + ''.join(random.choices(string.digits, k=random.randint(1, 4)))
    elif strategy == 'firstname_lastname':
        # Combined first and last name
        login = fake.first_name().lower() + fake.last_name().lower()
    elif strategy == 'email_prefix':
        # Username portion of email address
        login = fake.email().split('@')[0]
    else:
        # Random letters with 2 digits at end
        length = random.randint(5, 12)
        login = ''.join(random.choices(string.ascii_lowercase, k=length-2))
        login += ''.join(random.choices(string.digits, k=2))

    return login

def generate_unique_logins(count, output_file=DATA_PATH):
    """
    Input: count (int) - Number of unique logins to generate, output_file (str) - Output file path
    Output: None
    Generates unique login names and writes them sorted to a file.
    """
    logins = set()
    attempts = count * 2  # Try up to 2x the count to ensure uniqueness

    # Generate unique logins using a set to avoid duplicates
    for _ in tqdm(range(attempts), desc='Generating logins'):
        logins.add(generate_login())
        if len(logins) >= count:
            break

    # Write sorted logins to file
    with open(output_file, 'w') as f:
        for login in tqdm(sorted(logins), desc='Writing to file'):
            f.write(login + '\n')

    print(f'Generated {len(logins)} unique logins to {output_file}')

if __name__ == '__main__':
    # Generate 10 million unique logins
    generate_unique_logins(10000000, DATA_PATH)
