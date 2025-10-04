from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
import os
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_delete
from django.dispatch import receiver
import cloudinary

def blog_preview_upload_to(instance, filename):
    title_slug = slugify(instance.title)
    return os.path.join(title_slug, 'previewimage', filename)

def section_image_upload_to(instance, filename):
    post_slug = slugify(instance.section.blog_post.title)
    section_slug = slugify(instance.section.title)
    return os.path.join(post_slug, section_slug, 'photos', filename)

def section_video_upload_to(instance, filename):
    post_slug = slugify(instance.section.blog_post.title)
    section_slug = slugify(instance.section.title)
    return os.path.join(post_slug, section_slug, 'videos', filename)

def news_preview_upload_to(instance, filename):
    title_slug = slugify(instance.title)
    return os.path.join('news', title_slug, filename)

def news_section_image_upload_to(instance, filename):
    post_slug = slugify(instance.section.blog_post.title)
    section_slug = slugify(instance.section.title)
    return os.path.join('news', post_slug, section_slug, filename)

class RegistrationCode(models.Model):
    code = models.CharField(max_length=32, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    registration_code = models.OneToOneField(RegistrationCode, null=True, blank=True, on_delete=models.CASCADE)

    objects = UserManager()

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    preview_image = CloudinaryField('image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=150)
    content = models.TextField(max_length=450)
    preview_image = CloudinaryField('image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Hír'
        verbose_name_plural = 'Hírek'

    def __str__(self):
        return self.title

class BlogSection(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=450)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.blog_post.title} - {self.title}"

class SectionImage(models.Model):
    section = models.ForeignKey(BlogSection, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image')

    def __str__(self):
        return f"Image for {self.section.title}"

class SectionVideo(models.Model):
    section = models.ForeignKey(BlogSection, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to=section_video_upload_to)

    def __str__(self):
        return f"Video for {self.section.title}"

class Event(models.Model):
    event_title = models.CharField(max_length=255)
    host = models.CharField(max_length=150)
    event_type = models.CharField(max_length=100)
    date = models.DateField()
    reward = models.BooleanField(default=False)
    location = models.CharField(max_length=255)
    campfire_link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.event_title} ({self.date})"

@receiver(post_delete, sender=BlogPost)
def delete_blogpost_image(sender, instance, **kwargs):
    if instance.preview_image:
        cloudinary.uploader.destroy(instance.preview_image.public_id)

@receiver(post_delete, sender=News)
def delete_news_image(sender, instance, **kwargs):
    if instance.preview_image:
        cloudinary.uploader.destroy(instance.preview_image.public_id)

@receiver(post_delete, sender=SectionImage)
def delete_sectionimage_image(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)
