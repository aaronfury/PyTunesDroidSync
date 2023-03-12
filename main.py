import flet
from flet import Page
from pytunesapp import PyTunesApp

def main(page: Page):
    page.title = "PyTunesDroidSync"
    page.padding = 20
    page.window_width = 840
    page.window_height = 640
    page.window_resizable = False
    page.window_center()
    page.window_to_front()
    page.update()

    app = PyTunesApp(page)
    page.add(app)

    app.initialize()

flet.app(target=main)