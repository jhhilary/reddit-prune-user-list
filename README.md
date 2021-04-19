# Reddit User List Prune
This script will go through a list of users and separate them out into a list of active, suspended, and deleted/shadowbanned users. This script is mainly useful for condensing a large subreddit-specific shadowban list, but may have other uses

### Python Version and OS
This has been tested using Python 3.9.2 installed using Homebrew on a Mac, but should work on other operating systems and Python versions. If you're not using Python 3 obviously the commands would be slightly different

### Usage
1. Set up `.env`

The script loads credentials from a `.env` file. Take the contents of `.env-placeholder`, replace the `placeholder` values with your credentials, and rename to `.env`

2. Set up `user-list.txt`

Paste the list you're looking to prune into `user-list-placeholder.txt` and rename to `user-list.txt`. This should just be a comma-separated list of users without surrounding brackets, with individual users optionally being surrounded by single or double quotes

3. Install requirements

`python3 -m pip install -r requirements.txt`

4. Execute script

`python3 user-prune.py`

The script will give a continuous progress update on how many users it has looked up. Once complete, it will output the three different lists (active, suspended, and deleted/shadowbanned) to the command line

### Acknowledgments
Thanks to u/green_flash from r/worldnews who provided some example Python scripts that used PRAW, as well as the starting point for the `get_redditor_state` func 