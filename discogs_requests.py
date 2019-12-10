import discogs_client
import numpy as np
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import pickle
import os


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
        self.current_url = None
        self.list_ids = None

    def init_client(self):
        """
        Initiates a Discogs API Client with the user_agent and the user_token
        """
        self.dsc = discogs_client.Client(self.user_agent, user_token=self.user_token)

    def search_release(self, release_id):
        """
        Searching a specific release via the Discogs API
        :param release_id: the id of the release
        """
        self.last_search = self.dsc.release(release_id)

    def search_user_url(self, user_name):
        """
        Searching a specific user via the Discogs API
        :param user_name: the name of the specified user
        :return: the parsed data url corresponding to that user
        """
        self.last_search = self.dsc.user(user_name)
        page = urlopen(self.last_search.data['resource_url'])
        soup = BeautifulSoup(page, "html.parser").encode('UTF-8')
        parsed = json.loads(soup)

        return parsed

    def init_recursion(self, user_name):
        """
        Initiating the recursive exploration
        :param user_name: the name of the specified user
        """
        self.last_search = self.dsc.user(user_name)
        self.current_url = self.last_search.collection_folders[0].releases.url

    def recursive_exploration(self):
        """
        Explores all the pages of the collection of the current user recursively
        :return: a boolean being True if there is another collection page, False if it was the last one
        """
        page = urlopen(self.current_url)
        soup = BeautifulSoup(page, "html.parser").encode('UTF-8')
        parsed_releases = json.loads(soup)

        # check if there is a next page, or if it is the last page
        if 'next' in parsed_releases['pagination']['urls']:
            there_is_next = True
            self.current_url = parsed_releases['pagination']['urls']['next']
        else:
            there_is_next = False

        list_releases = parsed_releases['releases']

        self.list_ids = [0]*len(list_releases)

        for index_release, release in enumerate(list_releases):
            self.list_ids[index_release] = release['id']

        return there_is_next

    def user_collection_recursive(self, user_name):
        """
        A method trying to implement a recursion-based model to cycle over all the pages of the items collection
        :param user_name: the name of the specified user
        :return: the list of ids of the collection of the user
        """
        self.init_recursion(user_name)
        list_ids = []

        while self.recursive_exploration():
            list_ids = list_ids + self.list_ids

        return list_ids

    def get_50_items(self, user_name):
        """
        Gets the first 50 items ids of the collection of the specified user.
        :param user_name: the name of the specified user
        :return: the list of items ids
        """
        print(user_name)

        self.current_url = 'https://api.discogs.com/users/' + user_name + '/collection/folders/0/releases'

        try:
            page = urlopen(self.current_url)
            has_been_opened = True

        except urllib.error.HTTPError:
            print('This User has a private collection')
            has_been_opened = False

        if has_been_opened:
            soup = BeautifulSoup(page, "html.parser").encode('UTF-8')
            list_releases = json.loads(soup)['releases']

            self.list_ids = [0]*len(list_releases)

            for index_release, release in enumerate(list_releases):
                self.list_ids[index_release] = release['id']
        else:
            self.list_ids = []

        return self.list_ids

    def init_users_list(self, users_list):
        """
        Initiates a users dictionary to make the correspondance between users names and indexes.
        Also initiates the users-to-users matrix
        :param users_list: the list of users names we want to treat
        """
        self.users_list = users_list
        self.number_users = len(users_list)
        self.collection_list = [0]*self.number_users
        self.u2u_matrix = -np.ones((self.number_users, self.number_users))

        for index_user, user in enumerate(users_list):
            self.dict_users[user] = index_user

    @staticmethod
    def user_collection_without_api(user_name):
        """
        Retrieves all the items in the collection of the specified user.
        :param user_name: the name of the specified user
        :return: the list of all the releases in the user's collection
        """
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
        """
        Retrieves the ids of all items within the collection of the specified user.
        :param user_name: the name of the user we want to get the items ids of
        :return: the list of ids for the items in the collection of the specified user
        """
        url_to_go = 'https://api.discogs.com/users/' + user_name + '/collection/folders/0/releases'
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
                for index_item in range(items % per_page):
                    real_index = index_item + per_page*index_page
                    list_releases_id[real_index] = current_parsed['releases'][index_item]['id']
            else:
                for index_item in range(per_page):
                    real_index = index_item + per_page*index_page
                    list_releases_id[real_index] = current_parsed['releases'][index_item]['id']

        return list_releases_id

    def build_collection_list(self):
        """
        Builds the list of all inventories of the users listed in the users_list
        :return: the list of all inventories of the users in the users_list
        """
        for user_name in self.users_list:
            user_id = self.dict_users[user_name]
            self.collection_list[user_id] = self.get_50_items(user_name)

        return self.collection_list

    def build_user_matrix(self):
        """
        Builds the user-to-user matrix.
        Each cell is the number of common releases between the collections of two users.
        """
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

    def load_list_contributors(self, path):
        """
        Loads the pickle file containing the names of the top 5000 Discogs contributors.
        :param path: path to the pickle file
        """
        print(os.getcwd() + '/' + path)
        with open(os.getcwd() + '/' + path, 'rb') as input_file:
            self.users_list = pickle.load(input_file)

        self.init_users_list(self.users_list)


fake_users_list = ['thomzoy', 'mkvMafia', 'arli2001']

disco = DiscogsInstance()
disco.load_list_contributors('contributors.pickle')
# disco.init_users_list(fake_users_list)
disco.init_client()
disco.build_collection_list()
disco.build_user_matrix()
print(disco.u2u_matrix)
print()
