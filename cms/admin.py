from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(TeamMember)
admin.site.register(Contact)
admin.site.register(ContactFormSubmission)
admin.site.register(PageView)
