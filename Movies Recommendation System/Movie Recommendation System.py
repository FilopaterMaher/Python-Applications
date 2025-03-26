from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Optional


class Movie:
    """Represents a movie with an ID and a title."""
    
    def __init__(self, id: int, title: str):
        self._id = id
        self._title = title

    def get_id(self) -> int:
        return self._id

    def get_title(self) -> str:
        return self._title



class User:
    """Represents a user with an ID and a name."""
    
    def __init__(self, id: int, name: str):
        self._id = id
        self._name = name

    def get_id(self) -> int:
        return self._id



class MovieRating(Enum):
    NOT_RATED = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5



class IRatingRegister(ABC):
    """Interface for rating management."""

    @abstractmethod
    def add_rating(self, user: User, movie: Movie, rating: MovieRating):
        pass

    @abstractmethod
    def get_average_rating(self, movie: Movie) -> float:
        pass

    @abstractmethod
    def get_users(self) -> List[User]:
        pass

    @abstractmethod
    def get_movies(self) -> List[Movie]:
        pass

    @abstractmethod
    def get_user_movies(self, user: User) -> List[Movie]:
        pass

    @abstractmethod
    def get_movie_ratings(self, movie: Movie) -> Dict[int, MovieRating]:
        pass



class RatingRegister(IRatingRegister):
    """Manages users' movie ratings."""

    def __init__(self):
        self._user_movies: Dict[int, List[Movie]] = {}
        self._movie_ratings: Dict[int, Dict[int, MovieRating]] = {}
        self._movies: List[Movie] = []
        self._users: List[User] = []

    def add_rating(self, user: User, movie: Movie, rating: MovieRating):
        """Stores user rating for a movie."""
        if movie.get_id() not in self._movie_ratings:
            self._movie_ratings[movie.get_id()] = {}
            self._movies.append(movie)

        if user.get_id() not in self._user_movies:
            self._user_movies[user.get_id()] = []
            self._users.append(user)

        self._user_movies[user.get_id()].append(movie)
        self._movie_ratings[movie.get_id()][user.get_id()] = rating

    def get_average_rating(self, movie: Movie) -> float:
        """Calculates average rating for a movie."""
        if movie.get_id() not in self._movie_ratings:
            return MovieRating.NOT_RATED.value

        ratings = self._movie_ratings[movie.get_id()].values()
        return sum(r.value for r in ratings) / len(ratings)

    def get_users(self) -> List[User]:
        return self._users

    def get_movies(self) -> List[Movie]:
        return self._movies

    def get_user_movies(self, user: User) -> List[Movie]:
        return self._user_movies.get(user.get_id(), [])

    def get_movie_ratings(self, movie: Movie) -> Dict[int, MovieRating]:
        return self._movie_ratings.get(movie.get_id(), {})



class IMovieRecommender(ABC):
    """Interface for movie recommendation strategy."""

    @abstractmethod
    def recommend_movie(self, user: User) -> Optional[str]:
        pass


class MovieRecommendation(IMovieRecommender):
    """Movie recommendation system based on similarity scores."""

    def __init__(self, ratings: IRatingRegister):
        self._ratings = ratings

    def recommend_movie(self, user: User) -> Optional[str]:
        """Recommends a movie for a user based on ratings."""
        if not self._ratings.get_user_movies(user):
            return self._recommend_for_new_user()
        return self._recommend_for_existing_user(user)

    def _recommend_for_new_user(self) -> Optional[str]:
        """Suggests highest-rated movie for new users."""
        return max(self._ratings.get_movies(), key=self._ratings.get_average_rating, default=None)

    def _recommend_for_existing_user(self, user: User) -> Optional[str]:
        """Suggests a movie based on user similarity."""
        best_movie, lowest_score = None, float("inf")

        for reviewer in self._ratings.get_users():
            if reviewer.get_id() == user.get_id():
                continue

            score = self._calculate_similarity(user, reviewer)
            if score < lowest_score:
                lowest_score = score
                best_movie = self._find_unwatched_movie(user, reviewer)

        return best_movie.get_title() if best_movie else None

    def _calculate_similarity(self, user1: User, user2: User) -> int:
        """Calculates similarity between two users based on movie ratings."""
        common_movies = set(self._ratings.get_user_movies(user1)) & set(self._ratings.get_user_movies(user2))
        return sum(abs(self._ratings.get_movie_ratings(movie)[user1.get_id()].value -
                       self._ratings.get_movie_ratings(movie)[user2.get_id()].value)
                   for movie in common_movies) or float("inf")

    def _find_unwatched_movie(self, user: User, reviewer: User) -> Optional[Movie]:
        """Finds a movie watched by reviewer but not by the user."""
        user_movies = set(self._ratings.get_user_movies(user))
        reviewer_movies = self._ratings.get_user_movies(reviewer)

        best_movie, best_rating = None, 0
        for movie in reviewer_movies:
            if movie not in user_movies and self._ratings.get_movie_ratings(movie).get(reviewer.get_id(), MovieRating.NOT_RATED).value > best_rating:
                best_movie = movie
                best_rating = self._ratings.get_movie_ratings(movie)[reviewer.get_id()].value

        return best_movie


if __name__ == "__main__":
    user1, user2, user3 = User(1, "Alice"), User(2, "Bob"), User(3, "Charlie")
    movie1, movie2, movie3 = Movie(1, "Inception"), Movie(2, "Titanic"), Movie(3, "The Matrix")

    ratings = RatingRegister()
    ratings.add_rating(user1, movie1, MovieRating.FIVE)
    ratings.add_rating(user1, movie2, MovieRating.TWO)
    ratings.add_rating(user2, movie2, MovieRating.THREE)
    ratings.add_rating(user2, movie3, MovieRating.FOUR)

    recommender = MovieRecommendation(ratings)

    print(recommender.recommend_movie(user1))  # The Matrix
    print(recommender.recommend_movie(user2))  # Inception
    print(recommender.recommend_movie(user3))  # Inception
