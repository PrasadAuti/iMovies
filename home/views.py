from http.client import HTTPResponse
from django.http import HttpResponse
import json
from django.shortcuts import render
import pickle
import pandas as pd
import requests
from newsapi.newsapi_client import NewsApiClient
from home.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


def index(request): 
    if request.session.get('movieName') is not None:
        # Get a session value
        movieName = request.session['movieName']
        recommended_movie_names,recommended_movie_posters = recommend(movieName)
        rposter9=recommended_movie_posters[0]
        rtitle9=recommended_movie_names[0]

        rposter10=recommended_movie_posters[1]
        rtitle10=recommended_movie_names[1]

        rposter11=recommended_movie_posters[2]
        rtitle11=recommended_movie_names[2]

        rposter12=recommended_movie_posters[3]
        rtitle12=recommended_movie_names[3]
    else:
        rposter9,rtitle9,votes21,tagline1,overview1,revenue1,releaseDate1,runTime1=fetch_poster1(293660)
        rposter10,rtitle10,votes21,tagline1,overview1,revenue1,releaseDate1,runTime1=fetch_poster1(329)
        rposter11,rtitle11,votes21,tagline1,overview1,revenue1,releaseDate1,runTime1=fetch_poster1(37724)
        rposter12,rtitle12,votes21,tagline1,overview1,revenue1,releaseDate1,runTime1=fetch_poster1(122906)

    context ={
        # recommanded movies
        'rimg1':rposter9,
        'rtitle1':rtitle9,

        'rimg2':rposter10,
        'rtitle2':rtitle10,

        'rimg3':rposter11,
        'rtitle3':rtitle11,

        'rimg4':rposter12,
        'rtitle4':rtitle12,

        # top movies
        'img01':poster01,
        'title01':title01,
        'vote01':votes01,

        'img02':poster02,
        'title02':title02,
        'vote02':votes02,

        'img03':poster03,
        'title03':title03,
        'vote03':votes03,

        'img04':poster04,
        'title04':title04,
        'vote04':votes04,

        # mcu movies
        'img1':poster1,
        'title1':title1,
        'vote1':votes1,

        'img2':poster2,
        'title2':title2,
        'vote2':votes2,

        'img3':poster3,
        'title3':title3,
        'vote3':votes3,
        
        'img4':poster4,
        'title4':title4,
        'vote4':votes4,

        # dc movies
        'img5':poster5,
        'title5':title5,
        'vote5':votes5,

        'img6':poster6,
        'title6':title6,
        'vote6':votes6,

        'img7':poster7,
        'title7':title7,
        'vote7':votes7,

        'img8':poster8,
        'title8':title8,
        'vote8':votes8,

    }
    return render(request,'index.html',context)


def movie(request,movieName):

    movieId=movies[movies['title']==movieName].movie_id
    
    for i in movieId:
        mid=i
        print(mid)

    # for the main poster 
    poster1,title10,votes1,tagline1,overview1,revenue1,releaseDate1,runTime1 =fetch_poster1(mid)
    recommended_movie_names,recommended_movie_posters = recommend(movieName)

    img1=recommended_movie_posters[0]
    title1=recommended_movie_names[0]

    img2=recommended_movie_posters[1]
    title2=recommended_movie_names[1]

    img3=recommended_movie_posters[2]
    title3=recommended_movie_names[2]

    img4=recommended_movie_posters[3]
    title4=recommended_movie_names[3]

    context ={
        'img':poster1,
        'title':title10,
        'overview':overview1,
        'tagline':tagline1,
        'runTime':runTime1,
        'revenue':revenue1,
        'releaseDate':releaseDate1,
        'vote':votes1,

        'img1':img1,
        'title1':title1,
        'vote1':votes1,

        'img2':img2,
        'title2':title2,
        'vote2':votes2,

        'img3':img3,
        'title3':title3,
        'vote3':votes3,

        'img4':img4,
        'title4':title4,
        'vote4':votes4, 

    }
    return render(request,'movie.html',context)

def watch(request,movieName):
    movieId=movies[movies['title']==movieName].movie_id
    for i in movieId:
        mid=i
    recommended_movie_names,recommended_movie_posters = recommend(movieName)

    img1=recommended_movie_posters[0]
    title1=recommended_movie_names[0]

    img2=recommended_movie_posters[1]
    title2=recommended_movie_names[1]

    img3=recommended_movie_posters[2]
    title3=recommended_movie_names[2]

    img4=recommended_movie_posters[3]
    title4=recommended_movie_names[3]

    context ={
        'img1':img1,
        'title1':title1,
        'vote1':votes1,

        'img2':img2,
        'title2':title2,
        'vote2':votes2,

        'img3':img3,
        'title3':title3,
        'vote3':votes3,

        'img4':img4,
        'title4':title4,
        'vote4':votes4, 

        'movieName':movieName,
    }
    # Set a session value
    request.session['movieName']=movieName

    if request.user.is_authenticated:
        user_id = request.user.id
        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            profile = None
        if profile is not None and (profile.plan == "gold" or profile.plan == "silver" or profile.plan =="platinum"):
            if mid==87827:
                video_url="/static/assets/video/LifeOfPi.mp4"
                context2={"video_url": video_url}
                context.update(context2)
            elif mid==11036:
                video_url="/static/assets/video/TheNotebook.mp4"
                context2={"video_url": video_url}
                context.update(context2)
            elif mid==286217:
                video_url="/static/assets/video/TheMartian.mp4"
                context2={"video_url": video_url}
                context.update(context2)
            elif mid==32740:
                video_url="/static/assets/video/Krrish.mp4"
                context2={"video_url": video_url}
                context.update(context2)
            else: 
                video_url="/static/assets/video/goku.mp4"  
                context2={"video_url": video_url}
                context.update(context2)
            return render(request , 'renderMovie.html',context)
        else:
            messages.success(request, 'You have not Subscribed , Please select Plan.')
            return redirect('/subGold')

    else:
        messages.success(request, 'To watch movie, you have to Login first.')
        return redirect('/login')
    
# from pycharm

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_posters =[]
    recommended_movies =[]
    for i in movie_list:
        movie_id =movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster((movie_id)))
    return recommended_movies,recommended_movie_posters


movie_dict = pickle.load(open('static/movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('static/similarity.pkl','rb'))
# for Movie details form API

# for home
def fetch_poster1(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    title = data['title']
    votes = data['vote_average']
    tagline = data['tagline'] 
    overview = data['overview']
    releaseDate = data['release_date']
    runTime =data['runtime']
    revenue = data['revenue']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path,title,votes,tagline,overview,revenue,releaseDate,runTime


poster01,title01,votes01,tagline01,overview01,revenue01,releaseDate01,runTime01 =fetch_poster1(87827)
poster02,title02,votes02,tagline02,overview02,revenue02,releaseDate02,runTime02 =fetch_poster1(11036)
poster03,title03,votes03,tagline03,overview03,revenue03,releaseDate03,runTime03 =fetch_poster1(286217)
poster04,title04,votes04,tagline04,overview04,revenue04,releaseDate04,runTime04 =fetch_poster1(32740)

poster1,title1,votes1,tagline1,overview1,revenue1,releaseDate1,runTime1 =fetch_poster1(24428)
poster2,title2,votes2,tagline2,overview2,revenue2,releaseDate2,runTime2 =fetch_poster1(68721)
poster3,title3,votes3,tagline3,overview3,revenue3,releaseDate3,runTime3 =fetch_poster1(10195)
poster4,title4,votes4,tagline4,overview4,revenue4,releaseDate4,runTime4 =fetch_poster1(102899)


poster5,title5,votes5,tagline5,overview5,revenue5,releaseDate5,runTime5 =fetch_poster1(272)
poster6,title6,votes6,tagline6,overview6,revenue6,releaseDate6,runTime6 =fetch_poster1(49521)
poster7,title7,votes7,tagline7,overview7,revenue7,releaseDate7,runTime7 =fetch_poster1(297761)
poster8,title8,votes8,tagline8,overview8,revenue8,releaseDate8,runTime8 =fetch_poster1(155)


# for News

def news(request):
    newReq = requests.get(
        "https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=8e090dc59e2147caa228f64c081e2f4e"
    )
    api = json.loads(newReq.content)
    return render(request, 'news.html', context ={"api":api})

def newsCategory(request,category):
    newReq = requests.get(
        "https://newsapi.org/v2/top-headlines?country=in&category={}&apiKey=8e090dc59e2147caa228f64c081e2f4e".format(category)
    )
    api = json.loads(newReq.content)
    return render(request, 'newsCategory.html', context ={"api":api})
    
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/login')
        
        login(request , user)

        if request.session.get('movieName') is not None:
            # Get a session value
            movieName = request.session['movieName']
            return redirect(reverse('watch', kwargs={'movieName': movieName}))
            # return redirect('/watch/Life of Pi',movieName=movieName)
        else:
            return redirect('/')
    return render(request , 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(password)

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is already taken.')
                return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is already taken.')
                return redirect('/register')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request, 'registration.html')

def token_send(request):
    return render(request , 'token_send.html')


def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error(request):
    return render(request , 'error.html')

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi , click the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


@login_required(login_url='/login') 
def profile(request):
    return render(request,'profile.html')

def logoutUser(request):
    del request.session['movieName']
    logout(request)
    return redirect('/')

def subSilver(request):
    client = razorpay.Client(auth=("rzp_test_jMznWdL9PZWjxV", "R3eOyrpudMwTxvfGg7IgkWjF"))
    payment = client.order.create({'amount': 39900, 'currency': 'INR','payment_capture': '1'})
    return render(request,'subSilver.html')

def subGold(request):
    client = razorpay.Client(auth=("rzp_test_jMznWdL9PZWjxV", "R3eOyrpudMwTxvfGg7IgkWjF"))
    payment = client.order.create({'amount': 99900, 'currency': 'INR','payment_capture': '1'})
    return render(request,'subGold.html')

def subPlat(request):
    client = razorpay.Client(auth=("rzp_test_jMznWdL9PZWjxV", "R3eOyrpudMwTxvfGg7IgkWjF"))
    payment = client.order.create({'amount': 199900, 'currency': 'INR','payment_capture': '1'})
    return render(request,'subPlat.html')

def browse(request):
    if request.method == "POST":
        # name = request.POST.get('name')
        amount = 50000
        client = razorpay.Client(
            auth=("rzp_test_jMznWdL9PZWjxV", "R3eOyrpudMwTxvfGg7IgkWjF"))
        payment = client.order.create({'amount': 50000, 'currency': 'INR',
                                       'payment_capture': '1'})
    return render(request,'browse.html')

def error(request):
    return render(request , 'error.html')


def success(request):
    selectedPlan=request.GET.get('plan')
    try:
        userid=request.user.id
        profile_obj = Profile.objects.get(user_id = userid )

        if profile_obj:
            profile_obj.plan = selectedPlan
            profile_obj.save()

            # Get a session value
            movieName = request.session['movieName']
    
            return render(request,'success.html',{'plan':selectedPlan,'movieName':movieName})
        else:
            return redirect('/login')
    except Exception as e:
        print(e)
        return redirect('/error')
    
def search(request):
    if request.method=="POST":
        movieName=request.POST.get('searchKeyword')
    else:
        return render(request, 'error.html')
    try:
        movieId=movies[movies['title']==movieName].movie_id
    
        for i in movieId:
            mid=i
            print(mid)

        # for the main poster 
        poster1,title10,votes1,tagline1,overview1,revenue1,releaseDate1,runTime1 =fetch_poster1(mid)
        recommended_movie_names,recommended_movie_posters = recommend(movieName)

        img1=recommended_movie_posters[0]
        title1=recommended_movie_names[0]

        img2=recommended_movie_posters[1]
        title2=recommended_movie_names[1]

        img3=recommended_movie_posters[2]
        title3=recommended_movie_names[2]

        img4=recommended_movie_posters[3]
        title4=recommended_movie_names[3]

        context ={
            'img':poster1,
            'title':title10,
            'overview':overview1,
            'tagline':tagline1,
            'runTime':runTime1,
            'revenue':revenue1,
            'releaseDate':releaseDate1,
            'vote':votes1,

            'img1':img1,
            'title1':title1,
            'vote1':votes1,

            'img2':img2,
            'title2':title2,
            'vote2':votes2,

            'img3':img3,
            'title3':title3,
            'vote3':votes3,

            'img4':img4,
            'title4':title4,
            'vote4':votes4, 

        }
        return render(request,'movie.html',context)
    except:
        messages.success(request, 'Oops! movie not found , please check the spelling.')
        return redirect('/')
    
