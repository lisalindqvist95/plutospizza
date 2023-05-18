from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.urls import reverse

"""
Status for posts
"""
STATUS = ((0, "Draft"), (1, "Published"))

"""
Post Model below:
"""


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    restaurant = models.CharField(max_length=200, null=True)
    pizza = models.CharField(max_length=80, null=True)
    price = models.CharField(max_length=5, null=True)
    address = models.CharField(max_length=200, null=True)
    rating = models.IntegerField(default=0)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='blogpost_like', blank=True)

    class Meta:
        ordering = ["-created_on"]

    def get_absolute_url(self):
        """Get url after user adds/edits recipe"""
        return reverse('post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


"""
Comment Model below:
"""


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
