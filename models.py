from mongoengine import Document
from mongoengine.fields import StringField, DateField, ListField, ReferenceField
from locale import setlocale, LC_ALL
from datetime import datetime


setlocale(LC_ALL, 'en_US.UTF-8')


class Author(Document):
    fullname = StringField()
    born_date = DateField()
    born_location = StringField()
    description = StringField()

    def __init__(self, json_obj):
        super().__init__()
        self.fullname = json_obj["fullname"]
        self.born_date = datetime.strptime(json_obj["born_date"], "%B %d, %Y").date()
        self.born_location = json_obj["born_location"]
        self.description = json_obj["description"]


class Quote(Document):
    tags = ListField()
    author = ReferenceField(Author)
    quote = StringField()

    def __init__(self, json_obj):
        super().__init__()
        self.tags = json_obj["tags"]
        self.author = json_obj["author"]
        self.quote = json_obj["quote"]
