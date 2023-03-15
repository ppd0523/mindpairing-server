from google.cloud import storage
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from urllib.parse import quote_plus

from config import settings


@deconstructible
class FirebaseStorage(Storage):
    def __init__(self, **kwargs):
        self.client = storage.Client.from_service_account_info(settings.FIREBASE_INFO)
        self.bucket_name = settings.FIREBASE_STORAGE_BUCKET
        self.bucket = self.client.bucket(self.bucket_name)

    def _open(self, name, mode='rb'):
        raise NotImplementedError

    def _save(self, name, content):
        blob = self.bucket.blob(name)
        blob.upload_from_file(content.file, content_type='image/png')
        url = f'https://firebasestorage.googleapis.com/v0/b/{self.bucket_name}/o/{quote_plus(name)}?alt=media'
        return url

    def url(self, name):
        return f'{name}'

    def exists(self, name):
        blob = self.bucket.blob(name)
        return blob.exists()

    def delete(self, name):
        blob = self.bucket.blob(name)
        blob.delete()

    def size(self, name):
        blob = self.bucket.blob(name)
        return blob.size
