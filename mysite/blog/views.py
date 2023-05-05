from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView


# Create your views here.

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status = Post.Status.PUBLISHED,
                             slug = post,
                             publish__year = year, 
                             publish__month = month, 
                             publish__day = day)
    return render(request, 'blog/post/detail.html', {'post':post})

# def post_list(request):
#     post_list = Post.objects.all()
#     #постраничная разбивка по 3 поста на страницу
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get('page', 1)
#     #второе число в строке выше - дефолтное значение
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     #paginator.num_pages возвращает число,
#     #которое является количеством страниц
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     return render(request, 'blog/post/list.html', {'posts':posts})

#делает то же, что и закоментированная функция,
#только в виде класса
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'