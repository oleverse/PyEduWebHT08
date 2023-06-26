from mongoengine import Document
from mongoengine.fields import StringField, BooleanField, EmailField, ListField, ReferenceField, DateTimeField


class Contacts(Document):
    fullname = StringField(unique_with="email")
    email = EmailField(unique_with="fullname")
    got_message = BooleanField(default=False)
