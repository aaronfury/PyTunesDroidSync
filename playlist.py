from flet import Checkbox

class Playlist(Checkbox):
    def __init__(self,name) -> None:
        super().__init__(label=name)
        self.name = name
        self.items = []

    def __str__(self) -> str:
        return self.name