import random
import string

def generate_login(length_range=(5, 12)):
    length = random.randint(*length_range)

    names = [
        'james', 'john', 'robert', 'michael', 'william', 'david', 'richard', 'joseph', 'thomas', 'charles',
        'mary', 'patricia', 'jennifer', 'linda', 'elizabeth', 'barbara', 'susan', 'jessica', 'sarah', 'karen',
        'daniel', 'matthew', 'anthony', 'mark', 'donald', 'steven', 'paul', 'andrew', 'joshua', 'kenneth',
        'emily', 'ashley', 'amanda', 'melissa', 'deborah', 'stephanie', 'rebecca', 'laura', 'sharon', 'cynthia',
        'chris', 'alex', 'sam', 'jordan', 'taylor', 'morgan', 'riley', 'casey', 'jamie', 'charlie',
        'admin', 'user', 'test', 'demo', 'guest', 'root', 'dev', 'prod', 'bob', 'alice', 'jane'
    ]

    strategy = random.choice(['name_numbers', 'name_only', 'name_underscore_numbers', 'letters_numbers'])

    if strategy == 'name_numbers':
        login = random.choice(names) + ''.join(random.choices(string.digits, k=random.randint(1, 4)))
    elif strategy == 'name_only':
        login = random.choice(names)
        if random.random() > 0.5:
            login += random.choice(names)
    elif strategy == 'name_underscore_numbers':
        login = random.choice(names) + '_' + ''.join(random.choices(string.digits, k=random.randint(2, 4)))
    else:
        login = ''.join(random.choices(string.ascii_lowercase, k=length-2))
        login += ''.join(random.choices(string.digits, k=2))

    return login

def generate_unique_logins(count, output_file='logins.txt'):
    logins = set()
    while len(logins) < count:
        logins.add(generate_login())

    with open(output_file, 'w') as f:
        for login in sorted(logins):
            f.write(login + '\n')

    print(f'Generated {count} unique logins to {output_file}')

if __name__ == '__main__':
    generate_unique_logins(1000000, 'logins.txt')
