from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST


# Create your views here.

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status = Post.Status.PUBLISHED,
                             slug = post,
                             publish__year = year, 
                             publish__month = month, 
                             publish__day = day)
    comments = post.comments.filter(active = True)
    form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post':post, 'comments':comments, 'form':form})

def post_share(request, post_id):
    #пост извлекается по его id
    post = get_object_or_404(Post, id = post_id, status = Post.Status.PUBLISHED)
    
    sent = False
    
    if request.method == 'POST':
        #форма отправлена
        form = EmailPostForm(request.POST)
        #если поля формы успешно прошли валидацию
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} recommends you read {post.title}'
            message = f'Read {post.title} at {post_url}\n\n {cd["name"]}\'s comments: {cd["comments"]}'
            send_mail(subject, message, 'forstudy546@gmail.com', [cd['to']])
            sent = True
    
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})
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

# -------------------
# Comments

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status = Post.Status.PUBLISHED)
    comment = None
    #Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        #сохранить комментарий не загружая в базу
        comment = form.save(commit=False)
        #установить пост для комментария
        comment.post = post
        #сохранить в базу данных полную форму
        comment.save()
    return render(request, 'blog/post/comment.html', {'post':post, 'form':form, 'comment':comment})