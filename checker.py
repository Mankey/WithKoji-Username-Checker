import requests
from colorama import Fore, Style
from multiprocessing import Pool



usernames = []

def load_usernames():
    global usernames
    with open('usernames.txt', 'r') as f:
        usernames = f.read().splitlines()

def write_to_file(username):
    with open('available.txt', 'a') as f:
        f.write(username + '\n')

def check(username):
    r = requests.get(f'https://rest.koji-api.com/v1/user/create/checkUsername?username={username}', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
    # print(r.text)
    if r.status_code == 200:
        if r.json()['usernameIsAvailable'] == False:
            print(f'{Fore.RED} Username {username} is taken! {Style.RESET_ALL}')
        else:
            print(f'{Fore.GREEN} Username {username} is available! {Style.RESET_ALL}')
            write_to_file(username)
            

if __name__ == '__main__':
    load_usernames()
    #pirnt (usernames)
    pool = Pool(100)
    results = [pool.apply_async(check, args=(username,)) for username in usernames]
    output = [p.get() for p in results]
    pool.close()