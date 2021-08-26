from io import BytesIO

from config.testing import register
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


@register
def uploaded_image(self):
    bytes_io = BytesIO()
    Image.new('RGB', size=(10, 10), color=(0, 255, 255)).save(bytes_io, 'GIF')
    bytes_io.seek(0)
    image_content = bytes_io.read()
    return SimpleUploadedFile('image.gif', image_content, 'image/gif')
