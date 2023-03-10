import os.path
import time
from libpytunes import Library
from playlist import Playlist
import flet
from flet import (
    Page,
    View,
    Column,
    Row,
    Icon,
    Text,
    Dropdown,
    ListView,
    ElevatedButton,
    BottomSheet,
    ProgressBar,
    UserControl,
    icons,
)

class PyTunesApp(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.xml_path = os.path.expanduser('~/Music/iTunes/iTunes Music Library.xml')
        self.itl = None
        self.target_devices = [flet.dropdown.Option("None")]
        self.playlists = []
        self.is_syncing = False
        
        self.text_xml_status = Text(
            value="XML not loaded"
        )

        self.target_device = Dropdown(
            options=self.target_devices,
            filled=True,
            label="Target MTP Device",
            value="None",
        )

        self.lv_playlists = ListView(
            controls=[
                Text(value="No playlists detected."),
            ],
            expand=True
        )

        self.lv_options = ListView(
            controls=[
                Text(value="No options available")
            ],
            expand=True
        )

        self.btn_sync = ElevatedButton(
            icon=icons.SYNC,
            text="SYNC",
            height=50,
            on_click=self.start_sync,
            disabled=self.is_syncing
        )

        self.btn_stop_sync = ElevatedButton(
            icon=icons.STOP_CIRCLE,
            text="STOP SYNC",
            height=50,
            on_click=self.stop_sync,
            disabled=not self.is_syncing
        )

        self.pb_sync_status = ProgressBar(
            width= 600,
            bar_height=16,
        )

        self.home_view = View(
            route='/',
            controls=[
                Row(
                    controls=[
                        self.text_xml_status,
                        self.target_device
                    ],
                    alignment= flet.MainAxisAlignment.SPACE_BETWEEN,
                    height=100,
                ),
                Row(
                    controls=[
                        Column(
                            controls=[
                                Text(
                                    "Playlists",
                                    size=20,
                                    weight="bold",
                                ),
                                self.lv_playlists,
                            ],
                            expand=1
                        ),
                        Column(
                            expand=1,
                        ),
                        Column(
                            controls=[
                                Text(
                                    "Options",
                                    size=20,
                                    weight="bold",
                                ),
                                self.lv_options
                            ],
                            expand=1
                        ),
                    ],
                    height=400,
                    alignment=flet.MainAxisAlignment.SPACE_BETWEEN
                ),
                self.btn_sync
            ]
        )
        self.sync_view = View(
            route='/sync',
            controls=[
                self.pb_sync_status,
                self.btn_stop_sync
            ]
        )
    
    def route_change(self, route):
        print(self.page.route)
        self.page.views.clear()
        self.page.views.append(
            self.home_view
        )
        if self.page.route == '/sync':
            self.page.views.append(
                self.sync_view
            )

    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)    

    def build(self):
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop

        return Column(
            expand=True,
            controls=self.home_view.controls
        )

    def initialize(self):
        self.load_library()

    def load_library(self):
        if os.path.isfile(self.xml_path):
            self.itl = Library(self.xml_path)
            self.text_xml_status.value = f"XML loaded at {time.strftime('%I:%M %p')}"
            self.text_xml_status.update()
        else:
            self.xml_status = "XML file not found"
            return
        
        self.playlists.clear()
        self.lv_playlists.controls.clear()
        for playlist_name in Library.getPlaylistNames(self.itl):
            if (playlist_name not in ("Downloaded","Audiobooks")):
                self.lv_playlists.controls.append(
                    Playlist(playlist_name)
                )
        self.lv_playlists.update()
    
    def start_sync(self, e):
        selected_playlists = filter(lambda playlist: playlist.value,self.lv_playlists.controls)
        for selected in selected_playlists:
            print(selected)
        self.is_syncing=True
        self.btn_sync.disabled=True
        self.btn_sync.update()
        self.page.go("/sync")
        self.btn_stop_sync.disabled=False
        self.btn_stop_sync.update()
    
    def stop_sync(self, e):
        self.is_syncing=False
        self.btn_sync.disabled=False
        self.btn_sync.update()
        self.btn_stop_sync.disabled=True
        self.btn_stop_sync.update()
        self.page.go("/")

    def persist_bottom_sheet(self,e):
        if (self.is_syncing):
            self.bs_sync.open=True
            self.bs_sync.update()