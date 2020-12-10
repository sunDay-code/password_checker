import requests
import hashlib

def request_api_data(query_char):
    # Utilize the api from pwnedpasswords.com
    url = 'https://api.pwnedpasswords.com/range/'+query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the Api')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h,c in hashes:
        if h == hash_to_check:
            return c
    return 0

def pwned_api_check(password):
    # encode the password and split. 
    sha1pw = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1pw[:5], sha1pw[5:]

    response = request_api_data(first5_char)
    return get_password_leaks_count(response,tail)

def main(passwords):
    for pw in passwords:
        count = pwned_api_check(pw)
        print(f"{pw} was found {count} times")


if __name__ == "__main__":
    filepath="passwords.txt"
    passwords=[]
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            passwords.append(line.rstrip())
            line = fp.readline()
    main(passwords)