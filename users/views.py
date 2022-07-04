from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.dispatch import receiver
from users.forms import EditProfileForm, MessageForm, RegisterForm
from compose.forms import CommentForm
from compose.models import LikedPost, Posts
from .models import Message, User,FriendRequest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

@login_required(login_url='login')
def Myprofile(request):
    account = request.user
    mypost = account.posts_set.all()

    page = request.GET.get('page')
    results = 10
    paginator = Paginator(mypost, results)

    try:
        mypost = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        mypost = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        mypost = paginator.page(page)

    friends = account.friends.all()[0:10]
    commentform = CommentForm()

    context = {'account':account, 'mypost':mypost, 'friends':friends, 'commentform':commentform,'pagonator':paginator}
    return render(request, 'users/profile.html',context)

@login_required(login_url='login')
def UserAccount(request, pk):
    user_account = User.objects.get(id=pk)
    userpost = user_account.posts_set.all()

    page = request.GET.get('page')
    results = 10
    paginator = Paginator(userpost, results)

    try:
        userpost = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        userpost = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        userpost = paginator.page(page)

    userfriends = user_account.friends.all()[0:10]
    commentform = CommentForm()

    context={'user_account':user_account,'userpost':userpost,'userfriends':userfriends, 'commentform':commentform,'paginator':paginator}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def SendRequest(request, pk):
    sender = request.user
    receiver = User.objects.get(id=pk)

    if request.method == "POST":
        friendrequst, created = FriendRequest.objects.get_or_create(
            sender = sender,
            receiver = receiver
        )
        if created:
            sender.sent_requests.add(receiver)
            receiver.received_requests.add(sender)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        else:
            return HttpResponse('Friend Request Already Sent')

    return render(request, 'compose/index.html')


@login_required(login_url='login')
def CancleRequest(request,pk):
    account = request.user
    receiver = User.objects.get(id=pk)
    friendrequest = FriendRequest.objects.get(sender=account,receiver=receiver)

    if request.method == "POST":
        friendrequest.delete()
        account.sent_requests.remove(receiver)
        receiver.received_requests.remove(account)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'compose/index.html')

@login_required(login_url='login')
def AcceptRequest(request,pk):
    account = request.user
    sender = User.objects.get(id=pk)
    friendrequest = FriendRequest.objects.get(sender=sender,receiver=account)

    if request.method == "POST":
        try:
            sender.friends.add(account)
            sender.blocked.remove(account)
        except:
            sender.friends.add(account)
        try:
            account.friends.add(sender)
            account.blocked.remove(sender)
        except:
            account.friends.add(sender)
        friendrequest.delete()
        sender.sent_requests.remove(account)
        account.received_requests.remove(sender)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    return render(request, 'compose/index.html')

@login_required(login_url='login')
def DeleteRequest(request, pk):
    account = request.user
    sender = User.objects.get(id=pk)
    friendrequest = FriendRequest.objects.get(sender=sender,receiver=account)

    if request.method == "POST":
        friendrequest.delete()
        sender.sent_requests.remove(account)
        account.received_requests.remove(sender)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'compose/index.html')


@login_required(login_url='login')
def Unfriend(request,pk):
    user = request.user
    get_user = User.objects.get(id=pk)
    
    if request.method == "POST":
        user.friends.remove(get_user)
        user.blocked.add(get_user)
        get_user.friends.remove(user)
        get_user.blocked.add(user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'users/profile.html')

@login_required(login_url='login')
def EditProfile(request):
    profile = request.user
    form = EditProfileForm(instance=profile)

    if request.method == "POST":
        form = EditProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid:
            form.save()
            return redirect('profile')
    context = {'form':form}

    return render(request, 'users/editprofile.html', context)

def Login(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    

    if request.method == "POST":
        email = request.POST['email'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exits')

        user = authenticate(request, email=email,password=password)

        if user is not None:
            login(request, user)
            # request.user.online = True
            # request.user.save()
            return redirect('home')
        else:
            messages.error(request, 'Username or password is not correct')

        
    return render(request, 'users/login-register.html')

def Logout(request):
    # request.user.online = False
    # request.user.save()
    logout(request)
    return redirect('login')

@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.online = True
    user.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.online = False
    user.save()

def Register(request):
    page = 'register'
    form = RegisterForm()

    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in')
        return redirect('home')

    if request.method == "POST":
        form = RegisterForm(request.POST)
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 and password2 and password1 != password2:
            messages.error(request, 'Password does not match')
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()

            subject = 'Welcome to Composa, A place to socialize'
            message = 'We are glad to have you in the community'
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Your account was created successfully')
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'An error occured during registration')
            

    context = {'page':page, 'form':form}
    return render(request, 'users/login-register.html', context)

@login_required(login_url='login')
def Messages(request,pk):
    sender = request.user
    recipient = User.objects.get(id=pk)
    friends = sender.friends.all()[0:3]
    message = Message.objects.filter(
        Q(sender=sender)&
        Q(recipient=recipient)|
        Q(sender=recipient)&
        Q(recipient=sender)
        )
    form = MessageForm()

    if request.method == "POST":
        form = MessageForm(request.POST,request.FILES)
        if form.is_valid:
            msg = form.save(commit=False)
            if not msg.body and not msg.image:
                return redirect('message', pk=recipient.id)
            msg.sender = sender
            msg.recipient = recipient
            msg.save()
            return redirect('message', pk=recipient.id)
    context = {'message':message,'form':form, 'friends':friends,'recipient':recipient}
    return render(request,'users/message.html', context)


@login_required(login_url='login')
def Received_request(request):
    user = request.user
    receive = user.received_requests.all()

    page = request.GET.get('page')
    results = 10
    paginator = Paginator(receive,results)

    try:
        receive = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        receive = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        receive = paginator.page(page)

    context = {'receive':receive,'paginator':paginator}
    return render(request,'users/request_receive.html',context)

@login_required(login_url='login')
def Sent_request(request):
    user = request.user
    send = user.sent_requests.all()

    page = request.GET.get('page')
    results = 10
    paginator = Paginator(send,results)

    try:
        send = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        send = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        send = paginator.page(page)

    context = {'send':send,'paginator':paginator}
    return render(request,'users/request_sent.html',context)

@login_required(login_url='login')
def Suggested_user(request):
    user = request.user
    send = user.sent_requests.all()
    receive = user.received_requests.all()
    friends = user.friends.all()
    users = User.objects.exclude(id__in=send).exclude(id__in = receive).exclude(username=user.username).exclude(id__in = friends)

    page = request.GET.get('page')
    results = 10
    paginator = Paginator(users,results)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        users = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        users = paginator.page(page)

    context = {'users':users,'paginator':paginator}
    return render(request,'users/suggested_user.html',context)

@login_required(login_url='login')
def Friends(request):
    user = request.user
    friends = user.friends.all()

    page = request.GET.get('page')
    results = 5
    paginator = Paginator(friends,results)

    try:
        friends = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        friends = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        friends = paginator.page(page)

    context = {'friends':friends,'paginator':paginator}
    return render(request,'users/friends.html',context)

@login_required(login_url='login')
def AccountFriends(request,pk):
    user = User.objects.get(id=pk)
    friends = user.friends.all()

    page = request.GET.get('page')
    results = 10
    paginator = Paginator(friends,results)

    try:
        friends = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        friends = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        friends = paginator.page(page)

    context = {'friends':friends,'paginator':paginator}
    return render(request,'users/friends.html',context)


@login_required(login_url='login')
def AllUsers(request):
    user = request.user
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    userslist = User.objects.filter(
        Q(username__icontains=q) |
        Q(name__icontains=q)
    ).exclude(username = user.username)

    context = {'userslist':userslist}
    return render(request,'users/userslist.html',context)

@login_required(login_url='login')
def BlockUser(request,pk):
    user = request.user
    account = User.objects.get(id=pk)

    if request.method == "POST":
        user.blocked.add(account)
        user.save()
        return redirect('user-account', pk=account.id)

    return render(request,'users/profile.html')

@login_required(login_url='login')
def UnBlockUser(request,pk):
    user = request.user
    account = User.objects.get(id=pk)

    if request.method == "POST":
        user.blocked.remove(account)
        user.save()
        return redirect('user-account', pk=account.id)

    return render(request,'users/profile.html')

@login_required(login_url='login')
def DeleteAccount(request):
    user = request.user

    if request.method == "POST":
        logout(request)
        user.delete()
        return redirect('login')

    context = {'obj':user}
    return render(request,'delete_account.html', context)



