from blog.models import Blog
from django.template import Context, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, Http404

def blog_posts(request):
    if ie_test(request):
        return fuck_ie(request)

    latest_blog_list = Blog.objects.all().order_by('-date_created')
    paginator = Paginator(latest_blog_list,2)

    page = request.GET.get('page')
    try:
        latest_blog_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first
        # page.
        latest_blog_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range
        # (e.g. 9999), deliver
        # last page of results.
        latest_blog_list = paginator.page(paginator.num_pages)

    c = {
        'pagetitle': 'blog',
        'latest_blogs': latest_blog_list,
        }

    if not request.is_ajax():
        return render(request, 'blog/base_blog_inf.html',c)
    
    return render(request, 'blog/base_blog.html',c)


def detail(request, blog_post_slug):
    if ie_test(request):
        return fuck_ie(request)
    
    blog_post = Blog.objects.get(slug=blog_post_slug)

    return render(request, 'blog/base_blog_post.html', {
        'blog_post': blog_post,
        'pagetitle': 'blog',
    })


def fuck_ie(request):
    t = loader.get_template('agora/base_text.html')
    ie_text = open('static/misc/ie.html','r')
    #ie_text = open('/srv/www/projectmed.org/static/misc/ie.html','r')
    text = ie_text.read()
    c = Context({
        'pagetitle': 'sorry',
        'text': text,
        })
    return HttpResponse(t.render(c))


def ie_test(request):
    agent = str(request.META['HTTP_USER_AGENT'])
    if (agent.find('MSIE') != -1) or (agent.find('msie') != -1):
        return True
    
