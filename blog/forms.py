from .models import Comment
from .models import Post
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    """ Create Recipe Form """
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

    class Meta:
        """
        Get recipe model, choose fields to display and add summernote widget
        """
        model = Post
        fields = [
            'title',
            'slug',
            'author',
            'featured_image',
            'excerpt',
            'restaurant',
            'pizza',
            'price',
            'address',
            'rating',
            'content',
        ]
    
    
