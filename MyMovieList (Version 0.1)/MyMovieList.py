import requests
import lxml
from bs4 import BeautifulSoup
import kivy
from kivy.app import App
from kivy.logger import RED
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage
from functools import partial

class Movie:
    def __init__(self, title, year, image, link):
        self.title = title
        self.year = year
        self.image = image
        self.link = "https://www.imdb.com"+link


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.rows = 2

        self.textInput = TextInput(multiline=False, halign="center")
        self.button = Button(text="Search", on_press=self.solve) 
        self.gridlayout = GridLayout(cols=2, size_hint_y=None, height=30)
        self.inside = GridLayout(cols=2)
        self.scroller = ScrollView(scroll_timeout=250, scroll_distance=20, do_scroll_y=True, do_scroll_x=False)

        self.add_widget(self.gridlayout)
        self.add_widget(self.inside)
        self.gridlayout.add_widget(self.textInput)
        self.gridlayout.add_widget(self.button)
       

    def solve(self, instance):
        title = self.textInput.text.replace(" ", "%20")
        URL = "https://www.imdb.com/find?q=" + title + "&s=tt&ttype=ft&ref_=fn_ft"

        html_content = requests.get(URL).text
        soup = BeautifulSoup(html_content, "lxml")

        try:
            self.inside.clear_widgets()
            data = html_content.split("table")
            data = data[1].split("<td class=\"primary_photo\">")
            data.pop(0)

            movies = []

            for movie in data:
                movies.append(Movie(movie.split(">")[6][:-3], movie.split(">")[7][1:-4], movie.split("\"")[3], movie.split("\"")[1]))

            for i in range(20):
                try:
                    self.inside.add_widget(AsyncImage(source=movies[i].image, size_hint_x=None, width=60))
                    self.inside.add_widget(Button(on_press=partial(self.printcheck, movies[i].link), text=movies[i].title + " " + movies[i].year))
                except:
                    break
        except:
            self.inside.add_widget(Label(text="No Result!"))

    def printcheck(self, movie, instance):
        print(movie)
        


class TheLabApp(App):
    def build(self):
        return MyGrid()


TheLabApp().run()