from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from appdashboard.helpers import *
from froala_editor.fields import FroalaField
# Create your models here.


TAG_CHOICES = (
    ('trending_first','trending_first'),
    ('trending','trending'),
    ('latest', 'latest'),
    ('editor1','editor1'),
    ('editor2','editor2'),
    ('popular','popular'),
)

class BlogModel(models.Model):
    title=models.CharField(max_length=1000)
    content = FroalaField(plugins=('align', 'char_counter', 'code_beautifier' ,'code_view','draggable', 'emoticons',
        'entities', 'file', 'font_size', 'fullscreen', 'image_manager', 'image', 'inline_style',
        'line_breaker', 'link', 'lists', 'paragraph_format', 'paragraph_style', 'quick_insert', 'quote', 'save', 'table',
        'url', 'video'))
    # content = models.TextField()
    tag=models.CharField(max_length=100,choices=TAG_CHOICES,default="latest")
    user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    slug=models.SlugField(max_length=1000,null=True,blank=True)
    image=models.ImageField(upload_to='media')
    created_date_time=models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(BlogModel, self).save(*args, **kwargs)