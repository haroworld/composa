from queue import Empty
from urllib import request
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from compose.forms import ComposForm,CommentForm,RePostForm
from .models import LikedPost, Posts
from users.models import User,FriendRequest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect

# Create your views here.

@login_required(login_url='login')
def index(request):
    account = request.user
    posts = Posts.objects.all()

    page = request.GET.get('page')
    results = 10
    paginator = Paginator(posts, results)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)
    
    friendrequest = FriendRequest.objects.filter(receiver=account)
    myrequest = FriendRequest.objects.filter(sender=account)
    friends = account.friends.all()
    sent = account.sent_requests.all()
    received = account.received_requests.all()
    exclude_friends = User.objects.exclude(id__in=friends).exclude(id = account.id)
    exclude_user = User.objects.exclude(id = account.id)

    friendrequestquery = friendrequest.values_list('sender__id', flat=True)
    myrequestquery = myrequest.values_list('receiver__id', flat=True)

    receive = User.objects.filter(id__in = friendrequestquery)[0:5]
    send = User.objects.filter(id__in = myrequestquery)[0:5]

    users = User.objects.exclude(id__in=sent).exclude(id__in = received).exclude(username=account.username).exclude(id__in = friends)[0:5]
    
    
    
    form = ComposForm()
    commentform = CommentForm()
    

    if request.method == "POST":
        form = ComposForm(request.POST, request.FILES)
        if form.is_valid():
           user = form.save(commit=False)
           user.owner = request.user
           user.save()
           if user.post_privacy == 'friends only':
               user.blocked_users.add(*exclude_friends)
           if user.post_privacy == 'only me':
               user.blocked_users.add(*exclude_user)

           
           return redirect('home')

    
    context = {'posts':posts,'form':form,'users':users,'receive':receive,'send':send ,'friends':friends, 'commentform':commentform, 'paginator':paginator}
    
    return render(request, 'compose/index.html',context)

@login_required(login_url='login')
def singlePost(request, pk):
    compose = Posts.objects.get(id=pk)
    comment = compose.comments.all()[0:10]
    commentform = CommentForm()


    context ={'compose':compose, 'comment': comment, 'commentform':commentform}
    return render(request, 'compose/single_post.html', context)

@login_required(login_url='login')
def commentPost(request, pk):
    post = Posts.objects.get(id=pk)
    commentform = CommentForm()
    

    if request.method == "POST":
        commentform = CommentForm(request.POST, request.FILES)
        if commentform.is_valid():
            comment = commentform.save(commit=False)
            if not comment.post_body and not comment.post_image:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            comment.owner = request.user
            comment.main_post = post
            comment.save()
            post.comments.add(comment)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    context = {'commentform':commentform}
    return render(request, 'compose/index.html', context)


@login_required(login_url='login')
def unComment(request, pk):
    getcomment = Posts.objects.get(id=pk)
    post = Posts.objects.get(comments = getcomment)

    if request.method == "POST":
        getcomment.delete()
        return redirect('single_post', pk=post.id)

    return render(request, 'compose/single_post.html', {'getcomment':getcomment})

@login_required(login_url='login')
def DeletePost(request):
    pk = request.POST['pk']
    post = Posts.objects.get(id=pk)

    if request.method == "POST":
        post.delete()
        return redirect('home')

    return render(request, 'compose/index.html')


@login_required(login_url='login')
def LikePost(request):
    user = request.user
    pk = request.POST['pk']
    post = Posts.objects.get(id=pk)
    
    if user in post.blocked_users.all():
        messages.error(request, 'You cant like this post')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    if user in post.owner.blocked.all():
        messages.error(request, 'You cant like this post')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if post.owner in user.blocked.all():
        messages.error(request, 'You cant like this post')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == "POST":
        likedpost = LikedPost.objects.create(
            likedby = request.user,
            post = post
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'compose/index.html')

@login_required(login_url='login')
def UnlikPost(request, pk):
    getpost = Posts.objects.get(id=pk)
    user = request.user
    like = LikedPost.objects.get(likedby=user,post=getpost)

    if user in getpost.blocked_users.all():
        messages.error(request, 'You cant unlike this post')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if user in getpost.owner.blocked.all():
        messages.error(request, 'You cant unlike this post')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if getpost.owner in user.blocked.all():
        messages.error(request, 'You cant unlike this post')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == "POST":
        like.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'compose/index.html')

@login_required(login_url='login')
def Repost(request, pk):
    user = request.user
    post = Posts.objects.get(id=pk)
    repostform = RePostForm()

    if user in post.blocked_users.all():
        messages.error(request, 'You cant repost this post')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    if user in post.owner.blocked.all():
        messages.error(request, 'You cant repost this post')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if post.owner in user.blocked.all():
        messages.error(request, 'You cant repost this post')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == "POST":
        repostform = RePostForm(request.POST,request.FILES)
        if repostform.is_valid():
            reposted = repostform.save(commit=False)
            reposted.owner = request.user
            reposted.main_post = post
            reposted.save()
            post.reposts.add(reposted)
            return redirect('home')

    context = {'repostform':repostform, 'post':post}
    return render(request, 'compose/repost.html', context)

@login_required(login_url='login')
def UndoRepost(request, pk):
    getpost = Posts.objects.get(id=pk)
    user = request.user
    recompos = getpost.reposts.get(owner=user)

    if user in getpost.blocked_users.all():
        messages.error(request, 'You cant undo repost this post')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    if user in getpost.owner.blocked.all():
        messages.error(request, 'You cant undo repost this post')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if getpost.owner in user.blocked.all():
        messages.error(request, 'You cant undo repost this post')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.method == "POST":
        recompos.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'compose/index.html')







    




