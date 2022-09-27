import requests
import lxml
from bs4 import BeautifulSoup

class Movie:
    def __init__(self, title, year, image, link):
        self.title = title
        self.year = year
        self.image = image
        self.link = "https://www.imdb.com"+link

#

title = input("Movie Search\nTitle: ").replace(" ", "%20")
URL = "https://www.imdb.com/find?q=" + title + "&s=tt&ttype=ft&ref_=fn_ft"

html_content = requests.get(URL).text
soup = BeautifulSoup(html_content, "lxml")

try:
    data = html_content.split("table")
    data = data[1].split("<td class=\"primary_photo\">")
    data.pop(0)

    movies = []

    for movie in data:
    
        movies.append(Movie(movie.split(">")[6][:-3], movie.split(">")[7][1:-4], movie.split("\"")[3], movie.split("\"")[1]))

    for movie in movies:
        print(movie.title + " " + movie.year)
except:
    print("No Result!")