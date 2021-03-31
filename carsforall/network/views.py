from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.auth.decorators import login_required
import datetime
from django.db import IntegrityError
from django.http import JsonResponse
import json



@login_required
def index(request):
    cars=Car.objects.all()
    return render(request, "network/index.html",{"cars":cars})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")



def profile(request,profile_id):
    profile=User.objects.get(pk=profile_id)
    history=History.objects.filter(user=profile)
    cars_owned=profile.cars_owned.all()
    return render(request,"network/profile.html",{"profile":profile,
        "history":history,"cars_owned":cars_owned})




def createlisting(request):
    if request.method=="GET":
        return render(request,"network/createlisting.html")
    elif request.method=="POST":
        user=request.user
        name=request.POST["carname"]
        rent=request.POST["Rent"]
        image=request.POST["url"]
        seats=int(request.POST["seats"])
        description=request.POST["description"]
        insurance=request.POST["insurance"]
        dents=request.POST["dents"]
        posted_on=datetime.datetime.now()

        insurance=True if str(insurance)=="Yes" else False
        dents= True if str(dents)=="Yes" else False

        car=Car(owner=user,name=name,rent=rent,image=image,description=description,
            insurance=insurance,dents=dents,posted_on=posted_on,seats=seats)
        car.save()
        return HttpResponseRedirect(reverse("index"))

def list(request,list_id):
    car=Car.objects.get(pk=list_id)
    history=History.objects.filter(car=car)
    iswishlist=request.user.wishlist.filter(id=list_id).exists()
    is_asked_forrent=request.user.asked_for_rent.filter(id=list_id).exists()
    current_renter=car.current_renter.all()

    if len(current_renter)>0:
        current_renter=current_renter[0]
    else:
        current_renter=None
    hist=[]
    for h in history:
        if h.user not in hist:
            hist.append(h.user)

    return render(request,"network/listing.html",{"car":car,"iswishlist":iswishlist,"is_asked_forrent":is_asked_forrent,"current_renter":current_renter,"history":hist})

def wishlist(request):
    if request.method=="GET":
        wishlist=request.user.wishlist.all()
        return render(request,"network/wishlist.html",{"wishlists":wishlist})

@csrf_exempt
def add_remove_wishlist(request):
    if request.method=="POST":

        data=json.loads(request.body)
        pk=data["list_pk"]
        exists=data["exists"]

        current_user=User.objects.get(username=request.user.username)
        wished_car=Car.objects.get(pk=pk)

        current_user.wishlist.remove(wished_car)
        if not exists:
            current_user.wishlist.add(wished_car)
        
        current_user.save()
        message="Added to wishlist" if not exists else "REmoved from wishlist"
        return JsonResponse({"message":message})


@csrf_exempt
def ask_for_rent(request):
    if request.method=="POST":

        data=json.loads(request.body)
        pk=data["car_pk"]
        exists=data["exists"]

        current_user=User.objects.get(username=request.user.username)
        car=Car.objects.get(pk=pk)

        car.renters_wished.remove(current_user)
        if not exists:
            car.renters_wished.add(current_user)

        
        car.save()
        message="added "  if not exists else "REmoved"
        return JsonResponse({"message":message})




def notification(request):
    
    user=User.objects.get(username=request.user.username)
    cars_own=user.cars_owned.all()
    #renters={}
    renters=[]
    u=[]
    for car in cars_own:
        names=car.renters_wished.all()
        

        if len(names)>0:
            #renters[car.name]=name
            u.append(names)
            u.append(car)
            renters.append(u)
            u=[]
    
    return render(request, "network/notification.html",{"rental_info":renters})

    

@csrf_exempt
def decline(request):

    if request.method=="POST":
        data=json.loads(request.body)
        name=data['name']
        carid=data['carid']
        user=User.objects.get(username=name)
        car=Car.objects.get(pk=carid)
        car.renters_wished.remove(user)
        #car.renters_wished.clear()
        car.save()
        return JsonResponse({"message":f"{name} removed from list of renters_wished for {car.name}"})


@csrf_exempt
def accept(request):

    if request.method=="POST":

        data=json.loads(request.body)
        name=data['name']
        carid=data['carid']
        user=User.objects.get(username=name)
        car=Car.objects.get(pk=carid)
        car.renters_wished.clear()
        

        #history=History(user=user,car=car,time_of_rent=datetime.datetime.now())
        #history.save()
        car.current_renter.add(user)
        car.curr_time_rent=datetime.datetime.now()
        car.status=False
        
        car.save()
        return JsonResponse({"message":f"{car} is currently rented to {user}"})


def statusOfCars(request):

    user=User.objects.get(username=request.user.username)
    car=user.cars_owned.all()
    r=[]
    for c in car:
        l=[]
        l.append(c)
        u=c.current_renter.all()
        if len(u)>0:
            l.append(u[0])
        else:
            l.append("No renters at present.")
        l.append(c.curr_time_rent)
        r.append(l)
    return render(request,"network/statusofcars.html",{"stat":r})


@csrf_exempt
def endrent(request):
    if request.method=="POST":
        data=json.loads(request.body)
        carid=data['carid']
        renter=data['name']

        car=Car.objects.get(pk=carid)
        user=User.objects.get(username=renter)
        #renter=car.current_renter.all()

        history=History(user=user,car=car,time_of_rent=car.curr_time_rent,time_of_endrent=datetime.datetime.now())
        history.save()

        #clearing the data area of the current_renter attribute in cars since rent is ended.
               
        car.current_renter.clear()
        car.curr_time_rent=None
        car.status= not car.status
        car.save()
        return JsonResponse({"message":f"{car} is UNRENTED"})
