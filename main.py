import platform
import os.path
import pickle
import time
import tkinter as tk
import tkinter.font as tkFont
from libpytunes import Library

system=platform.system()
xml_path=os.path.expanduser('~/Music/iTunes/iTunes Music Library.xml')

print(f'You are running {system} and your iTunes XML should be at {xml_path}')
print('Checking whether the iTunes XML library is present')
if os.path.isfile(xml_path):
	print('Huzzah! XML file found')
else:
	print('Drats! The XML file was not found. Please enable the "Share iTunes Library XML with other applications" setting in iTunes (under "Preferences | Advanced")')
	quit()

pickle_file="itl.p"
expiry=3600  # Refresh pickled file if older than
epoch_time=int(time.time())  # Now

if not os.path.isfile(pickle_file) or os.path.getmtime(pickle_file) + expiry < epoch_time:
    itl_source=Library(xml_path)
    pickle.dump(itl_source, open(pickle_file, "wb"))

itl=pickle.load(open(pickle_file, "rb"))

# GUI
# TODO: Move into separate class

window=tk.Tk()
window.title("PyTunesDroidSync")
window.geometry("800x600")
window.minsize(800,600)

window.option_add("*justify","left")
window.option_add("*sticky","ew")
window.option_add("*expand","yes")
window.option_add("*fill","both")

fntH1 = tkFont.Font(
	size=18
)
fntH2 = tkFont.Font(
	size=14
)
fntH3 = tkFont.Font(
	size=12,
	weight="bold"
)

frame_main = tk.Frame(window)
frame_main.pack(
	padx=10,
	pady=10
)

label_title = tk.Label(
	frame_main,
	text="PyTunesDroidSync",
	font=fntH1
)
label_title.grid(
	column=0,
	row=0
)

frame_pl = tk.Frame(frame_main)
frame_pl.grid(
	column=0,
	row=1
)

tk.Label(
	frame_pl,
	text="Playlists",
	font=fntH2
).pack()

playlist_select = {}
playlist_names = Library.getPlaylistNames(itl)

for name in playlist_names:
	playlist_select.update({
		name: tk.BooleanVar()
	})
	tk.Checkbutton(
		frame_pl,
		text=name,
		variable=playlist_select[name],
	).pack()

frame_status = tk.Frame(frame_main)
frame_status.grid(
	column=1,
	row=1
)

text_status = tk.Text(
	frame_status,
	width=50,
	height=200
	)
text_status.insert(tk.END,"Initializing")

window.mainloop()