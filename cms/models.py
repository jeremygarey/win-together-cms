from django.db import models
from ckeditor.fields import RichTextField


class BlogPost(models.Model):
    name = models.CharField(max_length=200)
    body = RichTextField()
    summary = models.CharField(max_length=1000)
    main_image = models.CharField(max_length=300)
    thumbnail_image = models.CharField(max_length=300)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    profile_image = models.CharField(max_length=300)
    job_title = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    short_bio = models.CharField(max_length=1000)
    long_bio = RichTextField()

    def __str__(self):
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=200)
    subscribed = models.BooleanField(default=False, blank=True)
    added = models.DateTimeField(auto_now_add=True)


class ContactFormSubmission(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    message = models.CharField(max_length=2000)
    date = models.DateTimeField(auto_now_add=True)
