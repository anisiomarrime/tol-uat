from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from dashboard.models import *
from django.views import generic
from django.shortcuts import render
from django.db.models import Q

import os
from django.conf import settings
from django.http import HttpResponse, Http404

def download(request, slug):
    path = 'dashboard/static/cert'
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/text")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
            return response
    raise Http404

class HowToBuyTemplateView(TemplateView):
    template_name = "how_to_buy.html"
    context_object_name = "how_to_buy"

    def get_context_data(self, **kwargs):
        context = super(HowToBuyTemplateView, self).get_context_data(**kwargs)
        return context

class HowToSellTemplateView(TemplateView):
    template_name = "how_to_sell.html"
    context_object_name = "how_to_sell"

    def get_context_data(self, **kwargs):
        context = super(HowToSellTemplateView, self).get_context_data(**kwargs)
        return context

class  SecuritySuggestionsTemplateView(TemplateView):
    template_name = "security_suggestions.html"
    context_object_name = "security_suggestions"

    def get_context_data(self, **kwargs):
        context = super(SecuritySuggestionsTemplateView, self).get_context_data(**kwargs)
        return context


class IndexWebTemplateView(TemplateView):
    template_name = "index_web.html"
    context_object_name = "index_web"

    def get_context_data(self, **kwargs):
        context = super(IndexWebTemplateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        context = IndexWebTemplateView.get_context_data(self, **kwargs)
        context['categories'] = Category.objects.all()
        context['products'] = Post.objects.filter(status=1)
        return render(request, 'index_web.html', context)


class PostWebTemplateView(TemplateView):
    template_name = "post_web.html"
    context_object_name = "post_web"

    def get_context_data(self, **kwargs):
        context = super(PostWebTemplateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, **kwargs):
        context = PostWebTemplateView.get_context_data(self, **kwargs)
        context['categories'] = Category.objects.all()
        query = Q(status=1)

        try:
            category = int(request.GET['category'])
            if category > 0:
                query.add(Q(category_id=category), Q.AND)
                context['categoria'] = Category.objects.get(id=category)
        except:
            pass

        try:
            seller = int(request.GET['seller'])
            if seller > 0:
                query.add(Q(seller_id=seller), Q.AND)
        except:
            pass

        try:
            query.add(Q(title__contains=request.GET['q']), Q.AND)
        except:
            pass

        posts = Post.objects.filter(query).order_by("-id").distinct()

        page = request.GET.get('page', 1)

        paginator = Paginator(posts, 5)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts

        return render(request, 'posts_web.html', context)

    def single(request, id):
        post = Post.objects.get(slug=id)
        post.views = post.views + 1
        post.save()
        post.photos = Photo.objects.filter(post = post)
        return render(request, 'post_web.html', {'post': post, 'categories':Category.objects.all(), 'posts': Post.objects.filter(category__id=post.category.id)})

    # def get_num_post(request,id):
    #     totPost=Post.objects.filter(seller=seller).count
    #     context['posts']=totPost
    #     return render(request,'post_web.html',context)


