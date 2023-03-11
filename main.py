import platform
import os.path
import pickle
import time
import flet
from flet import (
    Page,
    Container,
    Column,
    Row,
    Icon,
    Text,
    Dropdown,
    ListView,
    FloatingActionButton,
    UserControl,
    Checkbox,
    PopupMenuButton,
    PopupMenuItem,
    colors,
    icons,
    margin
)
from libpytunes import Library

class PyTunesApp(UserControl):
    def build(self):
        self.text_xml_status = Text(
            value=self.xml_status
        )
        self.target_device = Dropdown(
            options=self.target_devices,
            filled=True,
            label="Target MTP Device"
            
        )
        self.lv_playlists = ListView(
            expand=True,
            controls=[
                Text(value="No playlists detected.")
            ]
        )

        self.lv_options = ListView(
            expand=True,
            controls=[
                Text(value="No settings available")
            ]
        )

        return Column(
            expand=True,
            controls=[
                Row(
                    controls=[
                        self.text_xml_status,
                        self.target_device
                    ],
                    alignment= flet.MainAxisAlignment.SPACE_BETWEEN
                ),
                Row(
                    controls=[
                        self.lv_playlists,
                        self.lv_options
                    ],
                ),
                FloatingActionButton(icon=icons.SYNC, text="SYNC", on_click=self.sync_clicked)
            ]
        )

    xml_status = "XML not loaded"
    target_devices = [flet.dropdown.Option("None")]

    def sync_clicked(self, e):
        self.update()

def main(page: Page):
    page.title = "PyTunesDroidSync"
    page.padding = 40
    page.update()

    app = PyTunesApp()
    page.add(app)

flet.app(target=main)

system = platform.system()
xml_path = os.path.expanduser('~/Music/iTunes/iTunes Music Library.xml')
xml_loadtimestamp = None

print(f'You are running {system} and your iTunes XML should be at {xml_path}')
print('Checking whether the iTunes XML library is present')
if os.path.isfile(xml_path):
    print('Huzzah! XML file found')
else:
    print('Drats! The XML file was not found. Please enable the "Share iTunes Library XML with other applications" setting in iTunes (under "Preferences | Advanced")')
    quit()

def refresh_itl():
    global xml_path, xml_loadtimestamp, pickle_file
    itl_source=Library(xml_path)
    pickle.dump(itl_source, open(pickle_file, "wb"))

pickle_file="itl.p"
expiry=3600  # Refresh pickled file if older than
epoch_time=int(time.time())  # Now

if not os.path.isfile(pickle_file) or os.path.getmtime(pickle_file) + expiry < epoch_time:
    refresh_itl()

itl=pickle.load(open(pickle_file, "rb"))

playlist_names = Library.getPlaylistNames(itl)