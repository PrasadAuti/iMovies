from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
    path('',views.index, name='home'),
    path('browse',views.browse, name='browse'),
    path('index',views.index, name='index'),
    path('movie/<str:movieName>',views.movie, name='movie'),
    path('news',views.news, name='news'),
    path('newsCategory/<str:category>',views.newsCategory, name='newsCategory'),
    path('login', views.loginUser, name='login'),
    path('register', views.register, name='register'),
    path('token' , views.token_send , name="token_send"),
    path('verify/<auth_token>' , views.verify , name="verify"),
    path('error',views.error,name='errorpage'),
    path('watch/<str:movieName>',views.watch,name='watch'),
    path('profile',views.profile,name='profile'),
    path('logout',views.logoutUser,name='logout'),
    path('subSilver',views.subSilver,name='subscribe'),
    path('subGold',views.subGold,name='subscribe'),
    path('subPlatinum',views.subPlat,name='subscribe'),
    path('success',views.success,name='success'),
    path('search',views.search,name='search'),
]
