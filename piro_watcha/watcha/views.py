from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Comment, Score
from .forms import CommentForm, ScoreForm
import urllib.request
import json
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.generic import View
from .forms import UserForm, LoginForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def main(request):
    return render(request, 'watcha/watcha_main.html', )


def detail(request, title):
    movie = get_object_or_404(Movie, title=title)
    comment_list = Comment.objects.filter(movie_name=title)
    score_list = Score.objects.filter(movie_name=title)
    return render(request, 'watcha/watcha_detail.html', {'movie': movie, 'comment_list': comment_list, 'score_list': score_list})


def search(request):
    if request.method == 'GET':
        client_id = "Qecl29vHRGgGNd4hjiov"
        client_secret = "XGZwdGHHfy"

        q = request.GET.get('q')
        encText = urllib.parse.quote("{}".format(q))
        url = "https://openapi.naver.com/v1/search/movie?query=" + encText + "&display=10"  # json 결과
        movie_request = urllib.request.Request(url)
        movie_request.add_header("X-Naver-Client-Id", client_id)
        movie_request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(movie_request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            result = json.loads(response_body.decode('utf-8'))
            items = result.get('items')
            for item in items:
                item['title'] = item['title'].replace("<b>", "").replace("</b>", "")
            print(items)
            if items:
                high_item = items[0]
                for movie in items:
                    title = movie.get('title')
                    if Movie.objects.filter(title=title):
                        pass
                    else:
                        title = movie.get('title')
                        content = movie.get('subtitle')
                        poster = movie.get('image')
                        Movie.objects.create(title=title, content=content, poster=poster)  # 필드 생성/ 제공받는 api 저장
                print(Movie.objects.all())
                return render(request, 'watcha/watcha_search.html', {'high_item': high_item, 'items': items, })
            else:
                return render(request, 'watcha/watcha_no_search.html')

#코멘트 생성, 수정, 삭제
def comment_new(request, title):
    if Comment.objects.filter(movie_name=title, author=request.user):
        return redirect('watcha:comment_edit', title=title)
    else:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.comment = form.cleaned_data['comment']
                comment.star = form.cleaned_data['star']
                comment.movie_name = Movie.objects.get(title=title).title
                comment.save()
                return redirect('watcha:detail', title=comment.movie_name)
        else:
            form = CommentForm()
            movie = get_object_or_404(Movie, title=title)
        return render(request, 'watcha/watcha_comment.html', {'form': form, 'movie': movie})

def comment_edit(request, title):
    comment = get_object_or_404(Comment, movie_name=title, author=request.user)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.comment = form.cleaned_data['comment']
            comment.star = form.cleaned_data['star']
            comment.movie_name = Movie.objects.get(title=title).title
            comment.save()
            return redirect('watcha:detail', title=comment.movie_name)
    else:
        form = CommentForm(instance=comment)
        movie = get_object_or_404(Movie, title=title)
    return render(request, 'watcha/watcha_comment.html', {'form': form, 'movie': movie})

def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.title = comment.movie_name
    comment.delete()
    return redirect('watcha:detail', title=comment.title)

# 평점 추가, 수정, 삭제
def score_new(request, title):
    if Score.objects.filter(movie_name=title, author=request.user):
        return redirect('watcha:score_edit', title=title)
    else:
        if request.method == 'POST':
            form = ScoreForm(request.POST)
            if form.is_valid():
                score = form.save(commit=False)
                score.author = request.user
                score.star = form.cleaned_data['star']
                score.movie_name = title
                score.save()
                return redirect('watcha:score', title=score.movie_name)
        else:
            form = ScoreForm()
            movie = get_object_or_404(Movie, title=title)
        return render(request, 'watcha/watcha_score.html', {'form': form, 'movie': movie})

def score_edit(request, title):
    score = get_object_or_404(Score, movie_name=title, author=request.user)
    if request.method == "POST":
        form = ScoreForm(request.POST, instance=score)
        if form.is_valid():
            score = form.save(commit=False)
            score.author = request.user
            score.star = form.cleaned_data['star']
            score.movie_name = title
            score.save()
            return redirect('watcha:detail', title=score.movie_name)
    else:
        form = ScoreForm(instance=score)
        movie = get_object_or_404(Movie, title=title)
    return render(request, 'watcha/watcha_score.html', {'form': form, 'movie': movie})

def score_delete(request, pk):
    score = get_object_or_404(Score, pk=pk)
    score.title = score.movie_name
    score.delete()
    return redirect('watcha:detail', title=score.title)



def main(request):
    return render(request, 'watcha/watcha_main.html')


def profile(request):
    return render(request, 'watcha/watcha_profile.html')


def flavor(request):
    return render(request, 'watcha/watcha_flavor.html')


class UserFormView(View):
    form_class = UserForm
    templates_name = 'watcha/watcha_register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.templates_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)  # login
                    return redirect('watcha:main')

        return render(request, self.template_name, {'form': form})


def loginpage(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('watcha:main')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'watcha/watcha_login.html', {'form': form})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'watcha/watcha_main.html', context)
