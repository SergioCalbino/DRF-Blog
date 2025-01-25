from django.db import models
from django.db.models import SET_NULL
from users.models import User
from categories.models import Category

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    miniature = models.ImageField(upload_to='posts/images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    #defino la relacion con el usuario y ademas que si se elimina el usuario no se borre el post, solo queda sin user
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=SET_NULL, null=True)

    def __str__(self):
        return self.title


