from .models import Comment, Post
from django import forms


class CommentForm(forms.ModelForm):
    """ Create Comment Form """
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = forms.Textarea(attrs={'rows': 3})

    class Meta:
        """Get comment model, choose fields to display"""
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    """ Create Post Form """
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

    class Meta:
        """
        Get Post model, choose which fields to display
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
            'status',
        ]
