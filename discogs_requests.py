import discogs_client
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


class discogs_instance(object):

    def __init__(self):
        self.consumer_key = 'xhTPysTNbOaratTZVDXs'
        self.consumer_secret = 'aluUBfaChtVFsGKqQqrzVBLZmktGwPGc'
        self.user_agent = 'discogs_ada_project_606'
        self.user_token = 'GJINDHmPqlHJhPSEoGgQEArvnXDyJuZRwDkNQYdU'
        self.dsc = None
        self.last_search = None
        self.dict_users = dict()
        self.u2u_matrix = None

    def init_client(self):
        self.dsc = discogs_client.Client(self.user_agent, user_token=self.user_token)

    def search_release(self, release_id):
        # epiphany = 14002052
        self.last_search = self.dsc.release(release_id)

    def search_user_url(self, user_id):
        # thomzoy
        self.last_search = self.dsc.user(user_id)
        page1 = urlopen(self.last_search.data['resource_url'])
        soup1 = BeautifulSoup(page1, "html.parser").encode('UTF-8')
        parsed1 = json.loads(soup1)
        collection_folders_url = parsed1['collection_folders_url']

        page2 = urlopen(collection_folders_url)
        soup2 = BeautifulSoup(page2, "html.parser").encode('UTF-8')
        parsed2 = json.loads(soup2)

        page3 = urlopen(parsed2['folders'][0]['resource_url'])
        soup3 = BeautifulSoup(page3, "html.parser").encode('UTF-8')
        parsed3 = json.loads(soup3)

        print(parsed3)
        print()

    def search_user_inventory(self, user_id):
        # thomzoy
        self.last_search = self.dsc.user(user_id)
        inventory = self.last_search.inventory
        print(inventory.url)

    def init_users_list(self, users_list):
        number_users = len(users_list)
        self.u2u_matrix = np.zeros((number_users, number_users))

        for index_user, user in enumerate(users_list):
            self.dict_users[user] = index_user

    def user_collection_without_api(self, user_id):

        url_to_go = 'https://api.discogs.com/users/' + user_id +'/collection/folders/0/releases'
        page = urlopen(url_to_go)
        soup = BeautifulSoup(page, "html.parser").encode('UTF-8')
        parsed = json.loads(soup)

        per_page = parsed['pagination']['per_page']
        items = parsed['pagination']['items']
        number_pages = items//per_page + 1

        total_releases = []

        for index_page in range(number_pages):
            url_current_page = 'https://api.discogs.com/users/' + user_id + \
                               '/collection/folders/0/releases?per_page=' + str(per_page) +\
                               '&amp;page=' + str(index_page)
            current_soup = BeautifulSoup(urlopen(url_current_page), "html.parser").encode('UTF-8')
            current_parsed = json.loads(current_soup)
            total_releases = total_releases + current_parsed['releases']

        return total_releases

    def build_user_matrix(self):




fake_users_list = ['toto', 'JB', 'Alex', 'Jan']

disco = discogs_instance()
disco.init_client()
# total_releases = disco.user_collection_without_api('Diognes_The_Fox')
disco.init_users_list(fake_users_list)
print()
