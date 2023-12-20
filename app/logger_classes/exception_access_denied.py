from app.imports import *
from app.log import Exception
class Exception_Access_Denied(Exception):
    def __init__(self, *args, **kwargs):
        self.set_content("Отказано в доступе")
        super().__init__(*args, **kwargs)

    def set_content(self, content):
        self.content = content
