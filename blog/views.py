from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic, View
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import CommentForm, Comment


class PostList(generic.ListView):
    """Homepage view, pagination"""
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


class PostDetail(View):
    """Postdetails, posts and comments"""
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


class PostLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class UpdateComment(
        LoginRequiredMixin, UserPassesTestMixin,
        SuccessMessageMixin, generic.UpdateView):

    """
    Allow logged in users to edit their comments
    Credit AliOKeefe The Easy Eater,
    https://github.com/AliOKeeffe/PP4_My_Meal_Planner
    """
    model = Comment
    form_class = CommentForm
    template_name = 'update_comment.html'
    success_message = "Comment successfully edited"

    def form_valid(self, form):
        form.instance.name = self.request.user.username
        return super().form_valid(form)

    def test_func(self):
        """
        Prevents other users from editing the comment
        """
        comment = self.get_object()
        return comment.name == self.request.user.username

    def get_success_url(self):
        """ Return to post detail when the comment is updated"""
        post = self.object.post
        return reverse_lazy('post_detail', kwargs={'slug': post.slug})


class DeleteComment(
        LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """
    Allow logged in users to delete their comments
    Credit AliOKeefe The Easy Eater,
    https://github.com/AliOKeeffe/PP4_My_Meal_Planner
    """
    model = Comment
    template_name = 'delete_comment.html'
    success_message = "Comment successfully deleted"

    def test_func(self):
        """
        Prevent another user from deleting user's comments
        """
        comment = self.get_object()
        return comment.name == self.request.user.username

    def delete(self, request, *args, **kwargs):
        """
        Credit AliOKeefe The Easy Eater,
        https://github.com/AliOKeeffe/PP4_My_Meal_Planner who credits
        Credit: https://stackoverflow.com/questions/24822509/
        success-message-in-deleteview-not-shown
        """
        return super(DeleteComment, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        """ Return to post detail view when comment is deleted"""
        post = self.object.post
        return reverse_lazy('post_detail', kwargs={'slug': post.slug})
