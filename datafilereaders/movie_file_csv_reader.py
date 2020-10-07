import csv

from domainmodel.movie import Movie
from domainmodel.actor import Actor
from domainmodel.genre import Genre
from domainmodel.director import Director

class MovieFileCSVReader:
    def __init__(self, filename):
        self.__file_name = filename
        self.movie_full_details = []
    def read_csv_file(self):
        csv_file_contents = csv.reader(open(self.__file_name, mode='r', encoding='utf-8-sig'))
        boolean = True
        for row in csv_file_contents:
            if boolean:
                boolean = False
                continue
            temp_movie = Movie("","")
            temp_movie.id = int(row[0])-1
            temp_movie.title = row[1]
            genre_list = row[2].split(",")
            genre_list = [Genre(genre) for genre in genre_list]
            temp_movie.genres = genre_list
            temp_movie.description = row[3]
            temp_movie.director = Director(row[4])
            actor_list = row[5].split(",")
            actor_list = [Actor(actor) for actor in actor_list]
            temp_movie.actors = actor_list
            temp_movie.releaseDate = int(row[6])
            temp_movie.runtime_minutes = int(row[7])
            temp_movie.rating = float(row[8])
            temp_movie.metascore = row[11]
            self.movie_full_details.append(temp_movie)