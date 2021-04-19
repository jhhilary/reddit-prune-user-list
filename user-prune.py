import logging
import os
import praw
import sys

from dotenv import load_dotenv
from prawcore.exceptions import NotFound

# global reddit session
r = None
user_list_active, user_list_suspended, user_list_deleted_shadowed = ([],[],[])

def main():
    global r
    load_dotenv()

    logging.basicConfig(filename='user-prune.log', encoding='utf-8', level=logging.INFO)
    r = praw.Reddit(username=os.environ.get('USERNAME'),
                    password=os.environ.get('PASSWORD'),
                    user_agent=os.environ.get('USER_AGENT'),
                    client_id=os.environ.get('CLIENT_ID'),
                    client_secret=os.environ.get('CLIENT_SECRET'))

    user_list = convert_txt_to_list()

    for i, user in enumerate(user_list, start=1):
        sys.stdout.write("\rLooking up user {} of {}".format(i,len(user_list)))
        sys.stdout.flush()
        get_redditor_state(r, user)

    output_lists()

def convert_txt_to_list():
    with open('user-list.txt', 'r') as file:
        user_str = file.read().replace('\n', '').replace(' ', '').replace('"', '').replace("'", '')
    user_list = user_str.split(',')
    return user_list

def get_redditor_state(r, username):
    logging.info('Fetching profile of user {0} ...'.format(username))
    account = r.redditor(username)
    try: 
        if hasattr(account, 'id'):
            logging.info('User {0} appears to be active.'.format(username))
            user_list_active.append(username)
        elif hasattr(account, 'is_suspended'):
            logging.info('User {0} appears to have been suspended.'.format(username))
            user_list_suspended.append(username)
        else:
            logging.info('User {0} appears to have been shadowbanned or has deleted their account.'.format(username))
            user_list_deleted_shadowed.append(username)
    except KeyboardInterrupt:
        print('Interrupted')
        try: sys.exit(0)
        except SystemExit: os._exit(0)
    except NotFound:
        logging.info('User {0} appears to have been shadowbanned or has deleted their account.'.format(username))
        user_list_deleted_shadowed.append(username)

def output_lists():
    print("\nCompleted. Parsed lists below.")
    print("\nACTIVE - {} USERS".format(len(user_list_active)))
    print(user_list_active)
    print("\nSUSPENDED - {} USERS".format(len(user_list_suspended)))
    print(user_list_suspended)
    print("\nDELETED/SHADOWED - {} USERS".format(len(user_list_deleted_shadowed)))
    print(user_list_deleted_shadowed)

if __name__ == '__main__':
    main()