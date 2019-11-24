import discogs_client
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


class DiscogsInstance(object):

    def __init__(self):
        self.consumer_key = 'xhTPysTNbOaratTZVDXs'
        self.consumer_secret = 'aluUBfaChtVFsGKqQqrzVBLZmktGwPGc'
        self.user_agent = 'discogs_ada_project_606'
        self.user_token = 'GJINDHmPqlHJhPSEoGgQEArvnXDyJuZRwDkNQYdU'
        self.dsc = None
        self.last_search = None
        self.number_users = -1
        self.dict_users = dict()
        self.collection_list = None
        self.users_list = None
        self.u2u_matrix = None

    def init_client(self):
        self.dsc = discogs_client.Client(self.user_agent, user_token=self.user_token)

    def search_release(self, release_id):
        # epiphany = 14002052
        self.last_search = self.dsc.release(release_id)

    def search_user_url(self, user_id):
        # thomzoy
        self.last_search = self.dsc.user(user_id)
        page = urlopen(self.last_search.data['resource_url'])
        soup = BeautifulSoup(page, "html.parser").encode('UTF-8')
        parsed = json.loads(soup)

        return parsed

    def search_user_inventory(self, user_id):
        # thomzoy
        self.last_search = self.dsc.user(user_id)
        inventory = self.last_search.inventory
        print(inventory.url)

    def init_users_list(self, users_list):
        self.users_list = users_list
        self.number_users = len(users_list)
        self.collection_list = [0]*self.number_users
        self.u2u_matrix = -np.ones((self.number_users, self.number_users))

        for index_user, user in enumerate(users_list):
            self.dict_users[user] = index_user

    @staticmethod
    def user_collection_without_api(user_name):
        url_to_go = 'https://api.discogs.com/users/' + user_name +'/collection/folders/0/releases'
        page = urlopen(url_to_go)
        soup = BeautifulSoup(page, "html.parser").encode('UTF-8')
        parsed = json.loads(soup)

        per_page = parsed['pagination']['per_page']
        items = parsed['pagination']['items']
        number_pages = items//per_page + 1

        total_releases = []

        for index_page in range(number_pages):
            url_current_page = 'https://api.discogs.com/users/' + user_name + \
                               '/collection/folders/0/releases?per_page=' + str(per_page) +\
                               '&amp;page=' + str(index_page)
            current_soup = BeautifulSoup(urlopen(url_current_page), "html.parser").encode('UTF-8')
            current_parsed = json.loads(current_soup)
            total_releases = total_releases + current_parsed['releases']

        return total_releases

    @staticmethod
    def user_collection_ids(user_name):
        url_to_go = 'https://api.discogs.com/users/' + user_name +'/collection/folders/0/releases'
        page = urlopen(url_to_go)
        soup = BeautifulSoup(page, "html.parser").encode('UTF-8')
        parsed = json.loads(soup)

        per_page = parsed['pagination']['per_page']
        items = parsed['pagination']['items']
        number_pages = items//per_page + 1

        list_releases_id = [0]*items

        for index_page in range(number_pages):
            url_current_page = 'https://api.discogs.com/users/' + user_name + \
                               '/collection/folders/0/releases?per_page=' + str(per_page) +\
                               '&amp;page=' + str(index_page)
            current_soup = BeautifulSoup(urlopen(url_current_page), "html.parser").encode('UTF-8')
            current_parsed = json.loads(current_soup)

            if index_page == number_pages-1:
                for index_item in range(items%per_page):
                    real_index = index_item + per_page*index_page
                    list_releases_id[real_index] = current_parsed['releases'][real_index]['id']
            else:
                for index_item in range(per_page):
                    real_index = index_item + per_page*index_page
                    list_releases_id[real_index] = current_parsed['releases'][real_index]['id']

        return list_releases_id

    def build_collection_list(self):

        for user_name in self.users_list:
            user_id = self.dict_users[user_name]
            self.collection_list[user_id] = self.user_collection_without_api(user_name)

        return self.collection_list

    def build_user_matrix(self):

        for row in range(self.number_users):
            for column in range(self.number_users):

                if row == column:
                    self.u2u_matrix[row, column] = len(self.collection_list[row])
                elif self.u2u_matrix[column, row] != -1:
                    self.u2u_matrix[row, column] = self.u2u_matrix[column, row]
                else:
                    row_list = self.collection_list[row]
                    col_list = self.collection_list[column]
                    commonalities = set(row_list) - (set(row_list) - set(col_list))
                    self.u2u_matrix[row, column] = len(commonalities)


fake_users_list = ['thomzoy', 'Diognes_The_Fox']

disco = DiscogsInstance()
disco.init_client()
disco.init_users_list(fake_users_list)
disco.build_collection_list()
disco.build_user_matrix()
print(disco.u2u_matrix)
