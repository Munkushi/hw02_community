from django.shortcuts import render, get_object_or_404

from .models import Group, Post


#Главная страница
def index(request):
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
        'posts':posts,
    }
    return render(request, 'posts/index.html', context)


#Страница сообществ
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    # Функция get_object_or_404 получает по заданным критериям объект 
    # из базы данных или возвращает сообщение об ошибке, если объект не найден.
    # В нашем случае в переменную group будут переданы объекты модели Group,
    # поле slug у которых соответствует значению slug в запросе
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group':group,
        'posts':posts,
    }
    return render(request, 'posts/group_list.html', context)
    #return HttpResponse(f'Сообщество {slug}')