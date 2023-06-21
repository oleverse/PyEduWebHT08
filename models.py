from mongoengine import Document
from mongoengine.fields import StringField, DateField, ListField, ReferenceField


class Authors(Document):
    fullname = StringField(unique_with="born_date")
    born_date = DateField(unique_with="fullname")
    born_location = StringField()
    description = StringField()


class Quotes(Document):
    tags = ListField()
    author = ReferenceField(Authors)
    quote = StringField(unique_with="author")
