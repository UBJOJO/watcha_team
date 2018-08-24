from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Comment, Score, Genre, Director, Cast
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
from django.core import serializers
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder


# json_serializer = serializers.get_serializer("json")()
# auto_box = json_serializer.serialize(movie_list, ensure_ascii=False)


# Create your views here.

# box = []
# for a in Movie.objects.all():
#     box.append(a.title)


def main(request):
    comment_num = Comment.objects.count()
    return render(request, 'watcha/watcha_main.html', {'comment_num': comment_num})


# def score_new(request, title):
#     if Score.objects.filter(movie_name=title, author=request.user):
#         return redirect('watcha:score_edit', title=title)
#     else:
#         if request.method == 'POST':
#             form = ScoreForm(request.POST)
#             if form.is_valid():
#                 score = form.save(commit=False)
#                 score.author = request.user
#                 score.star = form.cleaned_data['star']
#                 score.movie_name = title
#                 score.save()
#                 return redirect('watcha:score', title=score.movie_name)
#         else:
#             form = ScoreForm()
#             movie = get_object_or_404(Movie, title=title)
#         return render(request, 'watcha/watcha_score.html', {'form': form, 'movie': movie})

def detail(request, title):
    comment_num = Comment.objects.count()
    movie = get_object_or_404(Movie, title=title)
    comment_list = Comment.objects.filter(movie_name=title)
    score_list = Score.objects.filter(movie_name=title)
    form = ScoreForm(request.POST)
    movie_director_set = movie.director_set.all()
    movie_cast_set = movie.cast_set.all()
    movie_genre_set = movie.genre_set.all()
    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            score = form.save(commit=False)
            score.author = request.user
            score.star = form.cleaned_data['star']
            score.movie_name = Movie.objects.get(title=title).title
            score.save()
            return redirect('watcha:detail', title=score.movie_name)

    else:
        return render(request, 'watcha/watcha_detail.html',
                      {'movie': movie, 'comment_list': comment_list, 'score_list': score_list,
                       'count': comment_num, 'form': form, 'movie_director_set': movie_director_set, 'movie_cast_set': movie_cast_set, 'movie_genre_set': movie_genre_set})



def search(request):
    # 장르 1~28 다 있는지 확인
    genre_dic = {1: "드라마", 2: "판타지", 3: "서부", 4: "공포", 5: "로맨스", 6: "모험", 7: "스릴러", 8: "느와르", 9: "컬트", 10: "다큐멘터리",
                 11: "코미디", 12: "가족", 13: "미스터리", 14: "전쟁", 15: "애니메이션", 16: "범죄", 17: "뮤지컬", 18: "SF", 19: "액션",
                 20: "무협", 21: "에로", 22: "서스펜스", 23: "서사", 24: "블랙코미디", 25: "실험", 26: "영화카툰", 27: "영화음악",
                 28: "영화패러디포스터"}
    for genre in genre_dic.values():
        if Genre.objects.filter(name=genre):
            pass
        else:
            Genre.objects.create(name=genre)
    if request.method == "GET":
        client_id = "Qecl29vHRGgGNd4hjiov"
        client_secret = "XGZwdGHHfy"
        q = request.GET.get('q')
        encText = urllib.parse.quote("{}".format(q))
        # 장르별로 다 저장
        for genre_key in list(genre_dic.keys()):
            url = "https://openapi.naver.com/v1/search/movie?query=" + encText + "&display=100" + "&genre=%d" % (genre_key) # json 결과
            print(genre_key)
            movie_request = urllib.request.Request(url)
            movie_request.add_header("X-Naver-Client-Id", client_id)
            movie_request.add_header("X-Naver-Client-Secret", client_secret)
            response = urllib.request.urlopen(movie_request)
            rescode = response.getcode()
            # 네이버에서 응답이 정상적으로 왔는지 체크
            if (rescode == 200):
                response_body = response.read()
                result = json.loads(response_body.decode('utf-8'))
                naver_movies = result.get('items')
            # naver에서 불러온 영화 문자열 수정
                for naver_movie in naver_movies:
                    naver_movie['title'] = naver_movie['title'].replace("<b>", "").replace("</b>", "")
                # 제목 기준으로 필터링, 기생성된 영화에 장르 추가
                if naver_movies:
                    print(naver_movies)
                    for naver_movie in naver_movies:
                        title = naver_movie.get('title')
                        if Movie.objects.filter(title=title):
                            # 장르 추가하는 부분, 네이버 api에서 장르 하나씩 밖에 검색안되서 무쓸모..
                            # genre = genre_dic.get(genre_key)
                            # print(genre)
                            # first_genre = get_object_or_404(Genre, name=genre)
                            # print(first_genre)
                            # if first_genre:
                            #     movie_query = get_object_or_404(Movie, title=title)
                            #     print(movie_query)
                            #     movie_query.genre_set.add(first_genre)
                            pass
                    # 네이버 api에서 제공한 정보 저장
                        else:
                            title = naver_movie.get('title')
                            content = naver_movie.get('subtitle')
                            poster = naver_movie.get('image')
                            pubDate = naver_movie.get('pubDate')
                            director_str = naver_movie.get('director')
                            print(director_str)
                            director_list = director_str.split('|')
                            cast_str = naver_movie.get('actor')
                            cast_list = cast_str.split('|')
                            genre = genre_dic.get(genre_key)
                            # 영화 - 장르 연결 및 database에 Movie 저장
                            genre_query = get_object_or_404(Genre, name=genre)
                            movie_query = Movie.objects.create(title=title, content=content,
                                                               poster=poster, pubDate=pubDate)
                            movie_query.genre_set.add(genre_query)
                            # 영화 - 감독 연결
                            print(director_list)
                            for director in director_list:
                                if not Director.objects.filter(name=director):
                                    Director.objects.create(name=director)
                                    director_query = get_object_or_404(Director, name=director)
                                    movie_query.director_set.add(director_query)
                            # 영화 - 출연진 연결
                            for cast in cast_list:
                                if not Cast.objects.filter(name=cast):
                                    Cast.objects.create(name=cast)
                                    cast_query = get_object_or_404(Cast, name=cast)
                                    movie_query.cast_set.add(cast_query)
                # json_serializer = serializers.get_serializer("json")()
                # movie_json = json_serializer.serialize(list_movie, ensure_ascii=False)

    # 검색결과 보여주기
        url = "https://openapi.naver.com/v1/search/movie?query=" + encText + "&display=10" # json 결과
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
            if items:
                high_item = items[0]
                return render(request, 'watcha/watcha_search.html',
                            {'high_item': high_item, 'items': items})
            else:
                return render(request, 'watcha/watcha_no_search.html')


# 코멘트 생성, 수정, 삭제
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
    print('뉴 스코어 시작')
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
                return redirect('watcha:detail', title=score.movie_name)
        else:
            form = ScoreForm()
            movie = get_object_or_404(Movie, title=title)
        return render(request, 'watcha/watcha_detail.html', {'form': form, 'movie': movie})


def score_edit(request, title):
    print('에디트 실행됨')
    score = get_object_or_404(Score, movie_name=title, author=request.user)
    if request.method == "POST":
        form = ScoreForm(request.POST, instance=score)
        if form.is_valid():
            score = form.save(commit=False)
            score.author = request.user
            score.star = form.cleaned_data['star']
            score.movie_name = Movie.objects.get(title=title).title
            score.save()
            return redirect('watcha:detail', title=score.movie_name)
    else:
        form = ScoreForm(instance=score)
        movie = get_object_or_404(Movie, title=title)
    return render(request, 'watcha/watcha_detail.html', {'form': form, 'movie': movie})


def score_delete(request, pk):
    score = get_object_or_404(Score, pk=pk)
    score.title = score.movie_name
    score.delete()
    return redirect('watcha:detail', title=score.title)


def profile(request):
    return render(request, 'watcha/watcha_profile.html')


def flavor(request):
    movie_list = Score.objects.filter(author=request.user)
    movie_list_seen = []
    for movie in movie_list:
        movie_list_seen.append(Movie.objects.filter(title=movie.movie_name))
    movie_list_not_seen = Movie.objects.all()
    for movie in movie_list_not_seen:
        if Score.objects.filter(movie_name=movie.title, author=request.user):
            movie_list_not_seen = movie_list_not_seen.exclude(title=movie.title)
    return render(request, 'watcha/watcha_flavor.html',
                  {'movie_list_seen': movie_list_seen, 'movie_list_not_seen': movie_list_not_seen})


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


def flower(request):
    return render(request, 'watcha/watcha_flower.html')


def moreEvaluation(request):
    movie_list = Score.objects.filter(author=request.user)
    movie_list_seen = []
    for movie in movie_list:
        movie_list_seen.append(Movie.objects.filter(title=movie.movie_name))
    movie_list_not_seen = Movie.objects.all()
    for movie in movie_list_not_seen:
        if Score.objects.filter(movie_name=movie.title, author=request.user):
            movie_list_not_seen = movie_list_not_seen.exclude(title=movie.title)
    return render(request, 'watcha/watcha_moreEvaluation.html',
                  {'movie_list_seen': movie_list_seen, 'movie_list_not_seen': movie_list_not_seen})