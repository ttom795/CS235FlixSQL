from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director

class Movie:
    def __init__(self, movieName, releaseDate):
        self.id = 0
        self.releaseDate = releaseDate
        self.title = movieName.strip()
        self.description = ""
        self.director = ""
        self.actors = []
        self.genres = []
        self.runtime_minutes = 0
        self.rating = 0
        self.metascore = 0

    def __repr__(self):
        movieReturn = self.title
        if self.title == "":
            return "<Movie None>"
        return f'<Movie {self.title}, {self.releaseDate}>'

    def __eq__(self, toCompare):
        return self.title + " " + str(self.releaseDate) == toCompare.title + " " + str(toCompare.releaseDate)

    def __lt__(self, toCompare):
        return self.title + " " + str(self.releaseDate) < toCompare.title + " " + str(toCompare.releaseDate)

    def __hash__(self):
        return hash(self.title + " " + str(self.releaseDate))

    def add_actor(self, actorToAdd):
        self.actors.append(actorToAdd)

    def remove_actor(self, actorToRemove):
        if actorToRemove in self.actors:
            self.actors.remove(actorToRemove)

    def add_genre(self, genreToAdd):
        self.genres.append(genreToAdd)

    def remove_genre(self, genreToRemove):
        if genreToRemove in self.genres:
            self.genres.remove(genreToRemove)

    def __setattr__(self, name, value):
        if name == "runtime_minutes" and value < 0:
            raise ValueError("Runtime must be more than zero minutes")
        if name == "description":
            value = value.strip()
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)