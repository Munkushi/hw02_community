from django.shortcuts import redirect, render, get_object_or_404

from .models import Group, Post

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.core.paginator import Paginator

from django.contrib.auth import get_user_model

from .forms import PostForm

User = get_user_model()


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj,
        'group':group,
    }
    return render(request, 'posts/group_list.html', context)

@login_required
def profile(request, username):
    post_user_list = Post.objects.select_related('author', 'group').all()
    number_of_posts = post_user_list.count()
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  
    context = {'page_obj':page_obj,            
               'author':author,
               'post_list':post_list,
               'number_of_posts':number_of_posts,
    }
    return render(request, 'posts/profile.html', context)

@login_required
def post_detail(request,  post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_count = post.author.posts.count()
    context = {
        'post':post,
        'post_count':post_count,
        }
    return render(request, 'posts/post_detail.html', context)

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # ?????????? ???????????? = ?????????????? ??????????
            # instance = ???????????????????????????? ???????? ?????????????????????? ???????????? 
            form.instance.author = request.user
            form.save()
            return redirect('posts:profile', request.user)
        return render(request, 'posts/create_post.html', {'form':form}) 
    form = PostForm()
    return render (request, 'posts/create_post.html', {'form':form})



#@login_required
#def post_edit(request, post_id):
    #if request.method == 'GET': 
        #post = get_object_or_404(Post, pk=post_id)
        #form = PostForm(instance=post)
        #return render(request, 'posts/update_post.html', {'form':form})
    #elif request.method == 'POST':
        #form = PostForm(request.POST)
       # if form.is_valid():
            #form.instance.author = request.user
            #form.save()
            #return redirect('posts:profile', request.user.username)
        #return render(request, 'posts/update_post.html', {'form':form}) 

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post_id)
        else:
            context = {'form':form, 'is_edit':True}
            return render(request, 'posts/create_post.html', context)
    else:
        form = PostForm(instance=post)
        return render(request, 'posts/create_post.html', {'form':form})
