


# view page when user came in like the users view calling functions

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# this is for making your things in database through models work
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm



# this is the login functions

def loginPage(request):
    
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Doesnt exist')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
              messages.error(request, 'Username or password doesnt exist')
            
            
    contex = {'page':page}
    return render(request, 'base/login_register.html', contex)


# this is the logout functions
def logoutUser(request):
    logout(request)
    return redirect('home')

# this is the register functions
def registerPage(request):
    form = MyUserCreationForm()
    
    if request.method == 'POST': # this is for settering right our registration area
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'something went wrong, try again')
            
    return render(request, 'base/login_register.html', {'form':form})


# this is the home page function
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
                                Q(topic__name__icontains=q) | 
                                Q(name__icontains=q) | 
                                Q(description__icontains=q)
                                )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    
    context = {'rooms': rooms, 
               'topics':topics, 
               'room_count':room_count,
               'room_messages':room_messages,
                }
    return render(request, 'base/home.html', context)



# rooms of our websites for different conversations

def room(request, pk):
    room  = Room.objects.get(id=pk)
    room_messages =room.message_set.all() # this is for the comments
    
    participants =room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
            
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    context = {'room': room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)



# this is for creating prile view
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    
    context = {'user':user, 
               'rooms':rooms, 
               'room_messages':room_messages, 
               'topics':topics}
    return render(request, 'base/profile.html', context)




# this for redirecting the user to log in for creating a room
@login_required(login_url= 'login')

# this is for creating the room
def createRoom(request):
    form = RoomForm(),
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


# this for redirecting the user to log in for updating a room
@login_required(login_url= 'login')

# this is for updating the room
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    #this is for not deleting or editing somethig which is not yours
    if request.user != room.host:
        return HttpResponse('you are not allowed here!') # end
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


# this is for deleting the room
@login_required(login_url= 'login')

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('you can not delete this')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})


# this is for deleting the comment
@login_required(login_url= 'login')

def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('you can not delete this')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})

# this is for user profile

@login_required(login_url= 'login')

def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
                
    return render(request, 'base/update-user.html', {'form':form})
    


# this is for our topics

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics':topics})




# this is for our recent activities

def activityPage(request):
    room_messages = Message.objects.all()
  
    return render(request, 'base/activity.html', {'room_messages':room_messages})














