import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from core.models import BlogPost, User

class CloudinaryUploadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com', password='testpass')

    def test_blogpost_image_upload_cloudinary(self):
        with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
            tmp.write(b'\x89PNG\r\n\x1a\n')
            tmp.seek(0)
            image = SimpleUploadedFile('test_cloudinary.png', tmp.read(), content_type='image/png')
            post = BlogPost.objects.create(author=self.user, title='Cloudinary Test', preview_image=image)
            url = post.preview_image.url
            print('Cloudinary URL:', url)
            self.assertIn('cloudinary', url)
