#!/usr/bin/python
# coding: utf-8

########################

import sys
import xbmc
import xbmcgui

from resources.lib.helper import *
from resources.lib.tmdb_utils import *

########################

class TMDBPersons(object):
    def __init__(self,call_request):
        self.tmdb_id = call_request['tmdb_id']
        self.local_movies = call_request['local_movies']
        self.local_shows = call_request['local_shows']
        self.result = {}

        if self.tmdb_id:
            self.result['person'] = self.get_person_details()
            self.result['movies'] = self.get_movie_list()
            self.result['tvshows'] = self.get_tvshow_list()
            self.result['images'] = self.get_person_images()

    def __getitem__(self, key):
        try:
            value = self.result[key]
            return value

        except KeyError:
            return

    def get_person_details(self):
        details = tmdb_item_details('person',self.tmdb_id)
        li = list()

        list_item = tmdb_handle_person(details)
        li.append(list_item)

        return li

    def get_movie_list(self):
        movies = tmdb_item_details('person',self.tmdb_id,'movie_credits')
        movies = movies['cast']
        movies = sort_dict(movies,'release_date',True)
        li = list()
        duplicate_handler = list()

        for item in movies:
            if item['id'] not in duplicate_handler:
                list_item = tmdb_handle_movie(item,self.local_movies)
                li.append(list_item)
                duplicate_handler.append(item['id'])

        return li

    def get_tvshow_list(self):
        tvshows = tmdb_item_details('person',self.tmdb_id,'tv_credits')
        tvshows = tvshows['cast']
        tvshows = sort_dict(tvshows,'first_air_date',True)
        li = list()
        duplicate_handler = list()

        for item in tvshows:
            if item['character'] and item['id'] not in duplicate_handler:
                list_item = tmdb_handle_tvshow(item,self.local_shows)
                li.append(list_item)
                duplicate_handler.append(item['id'])

        return li

    def get_person_images(self):
        images = tmdb_item_details('person',self.tmdb_id,'images',use_language=False)
        images = images['profiles']
        li = list()

        for item in images:
            list_item = tmdb_handle_images(item)
            li.append(list_item)

        return li