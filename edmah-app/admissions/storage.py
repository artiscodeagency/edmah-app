from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse


class PrivateDocumentStorage(FileSystemStorage):
    """Stores admission documents outside MEDIA_ROOT so they are never served
    by the public /media/ static route. Files are only reachable through the
    staff/owner-gated `serve_document` view."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('location', settings.PRIVATE_MEDIA_ROOT)
        super().__init__(*args, **kwargs)

    def url(self, name):
        return reverse('serve_admission_document') + f'?path={name}'


private_storage = PrivateDocumentStorage()
