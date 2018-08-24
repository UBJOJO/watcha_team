from django.urls import path
from . import views

app_name = 'watcha'

urlpatterns = [
    path('comment/<str:title>/', views.comment_new, name='comment'),
    path('comment_edit/<str:title>/', views.comment_edit, name='comment_edit'),
    path('comment_delete/<int:pk>/', views.comment_delete, name='comment_delete'),
    path('score/<str:title>/', views.score_new, name='score'),
    path('score_edit/<str:title>/', views.score_edit, name='score_edit'),
    path('score_delete/<int:pk>/', views.score_delete, name='score_delete'),
    path('', views.main, name='main'),
    path('detail/<str:title>/', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('flavor/', views.flavor, name='flavor'),
    path('loginpage/', views.loginpage, name='login'),
    path('newaccount/', views.UserFormView.as_view(), name='newaccount'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('flower/', views.flower, name='flower'),
]
