import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://yupest.github.io/nti/%D0%9D%D0%A2%D0%98-2022/films/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = []

movies = soup.find_all('div', {'class': 'movie-head'})

for movie in movies:
    movie_number = movie.find('span').text
    movie_title = movie.find('h1').text.replace(movie_number, '').strip()
    movie_genres = [genre.text for genre in movie.find_all('li', {'class': 'genre'})]
    movie_rating = movie.find('li', {'name': 'rating_film'}).text
    movie_emotions = [emotion.text for emotion in movie.find_all('li', {'class': 'emotion'})]
    movie_emotion_ratings = [emotion.find('div', {'class': 's-text'}).text for emotion in
                             movie.find_all('li', {'class': 'spo'})]

    table.append([movie_number, movie_title, ', '.join(movie_genres), movie_rating,
                  ', '.join([f'{emotion} {rating}' for emotion, rating in zip(movie_emotions, movie_emotion_ratings)])])


df = pd.DataFrame(table, columns=['Индекс', 'Название фильма', 'Жанры', 'Рейтинг фильма', 'Рейтинг эмоции'])


df.to_excel('movies.xlsx', index=False)
