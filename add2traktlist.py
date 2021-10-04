import trakt
from trakt.tv import TVShow
from trakt.movies import Movie
from trakt.users import UserList
import re
import time
import requests
import argparse
import config


def get_trakt_object(base_url, title, year=''):
    try:
        if year == '':
            url = base_url+'&t='+title
        else:
            url = base_url+'&t='+title+'&y='+year
        res = requests.get(url).json()
        if res['Type'] == 'series':
            return TVShow(title=res['Title'], imdb_id=res['imdbID'])
        elif res['Type'] == 'movie':
            return Movie(title=res['Title'], imdb_id=res['imdbID'])
    except:
        print(f'\x1b[91m[ERROR] Unable to add {title}({year})\x1b[0m')


def main():
    parser = argparse.ArgumentParser(description='Add content to TRAKT lists. By Ashish0804.')
    parser.add_argument('-l', '--list', dest='trakt_list', help='Provide TRAKT list name.', required=True)
    parser.add_argument('-f', '--file', dest='filename', help='Provide content txt file.', required=True)
    args = parser.parse_args()

    # Read Content from file.
    with open(args.filename, 'r') as f:
        lines = f.readlines()

    # Initiate Trakt object.
    trakt.core.AUTH_METHOD = trakt.OAUTH_AUTH
    my_client_id = config.my_client_id
    my_client_secret = config.my_client_secret
    trakt.init(config.username, client_id=my_client_id, client_secret=my_client_secret)
    traktList = UserList.get(args.trakt_list, config.username)

    # Set OMDBAPI url.
    base_url = 'http://www.omdbapi.com/?apikey=' + config.omdb_api_key

    # Populate list.
    for line in lines:
        match = re.search(r'(?P<title>.+?)\((?P<year>.*)\)', line)
        trakt_object = get_trakt_object(base_url, match.group('title').strip(), match.group('year').strip())
        if trakt_object:
            traktList.add_items(trakt_object)
            print(f'\x1b[92m[INFO] Added {trakt_object.title}\x1b[0m')
            time.sleep(1)


if __name__ == '__main__':
    main()
