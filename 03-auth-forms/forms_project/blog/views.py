from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import CommentForm, ContactForm

def post_list(request):
    posts = Post.objects.all().order_by('-published_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # handle comment form submission
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            # Redirect to avoid form re-submission
            return redirect('blog:post_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # use form.cleaned_data, e.g. send email or print
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # for demo, just pass these back
            return render(request, 'blog/contact_success.html', {'name': name})
    else:
        form = ContactForm()

    return render(request, 'blog/contact_form.html', {'form': form})

