from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
from .forms import BlogPostModelForm
from .models import BlogPost
from profiles.models import Profile
from datetime import datetime

#from ..forms import UserFrorm

# CRUD

# GET -> Retrieve / List

# POST -> Create / Update / DELETE

# Create Retrieve Update Delete


@login_required
def blog_post_list_view(request):
    # list out objects 
    # could be search
    profile = Profile.objects.get(user=request.user)
    qs_new = BlogPost.objects.filter(id__gt=profile.last_post_id).order_by('-id')
    qs_old = BlogPost.objects.filter(id__lte=profile.last_post_id).order_by('-id')
    # print('Eddig id:', profile.last_post_id)
    # print('új post db, ',len(qs_new))
    # print('régi post db, ',len(qs_old))
    qs = BlogPost.objects.order_by('-id')[0]
    # print(qs.id)
    if qs:
        profile.last_post_id = qs.id
        profile.save()
    # print('Most:', profile.last_post_id)

    template_name = 'blog/list.html'
    context = {'object_list': qs_new, 'object_list_old': qs_old}
    return render(request, template_name, context) 


# @login_required
@staff_member_required
def blog_post_create_view(request):
    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = BlogPostModelForm()
    template_name = 'form.html'
    context = {'form': form}
    return render(request, template_name, context)  


def blog_post_detail_view(request, slug):
    # 1 object -> detail view
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/detail.html'
    context = {"object": obj}
    return render(request, template_name, context)   

@staff_member_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    template_name = 'form.html'
    context = {"title": f"Update {obj.title}", "form": form}
    return render(request, template_name, context)  


@staff_member_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/delete.html'
    if request.method == "POST":
        obj.delete()
        return redirect("/blog")
    context = {"object": obj}
    return render(request, template_name, context)

def blog_post_count_view(request):
    if request.method == "GET" and request.is_ajax():
        last_post_seen = Profile.objects.get(user=request.user).last_post_id
        qs_new = BlogPost.objects.filter(id__gt=last_post_seen)
        count = len(qs_new)
        # print('count:', count)
        # return JsonResponse({'msg': 'siker', 'count': count})
        # html = f"<html><body>It is now  {count}</body></html>"
        # return HttpResponse(html)
        return JsonResponse({'msg': 'siker', 'count': count})









