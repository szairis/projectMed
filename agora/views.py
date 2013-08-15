from agora.models import Posting, Reply, Specialty
from agora.forms import PostingForm, ReplyForm, ViewForm, OwnerForm
from django.template import Context, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, render
from django.core.mail import send_mail, EmailMessage
from datetime import datetime, timedelta


def index(request):
    if ie_test(request):
        return fuck_ie(request)

    t = loader.get_template('agora/base_index.html')
    c = Context({
        'pagetitle': 'welcome',
        })
    return HttpResponse(t.render(c))
    #return HttpResponseRedirect(str(request.META['HTTP_USER_AGENT'])) # Redirect


def listings(request):
    if ie_test(request):
        return fuck_ie(request)
    
    latest_listing_list = Posting.objects.all().order_by('-date_modified')
    form = ViewForm() # Unbound form
    paginator = Paginator(latest_listing_list, 5)

    page = request.GET.get('page')
    try:
        latest_listing_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first
        # page.
        latest_listing_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range
        # (e.g. 9999), deliver
        # last page of results.
        latest_listing_list = paginator.page(paginator.num_pages)
    
    c = {
        'pagetitle': 'browse',
        'form': form,
        'latest_listings': latest_listing_list,
        }

    if not request.is_ajax():
        return render(request, 'agora/base_listings_inf.html',c)
    
    return render(request, 'agora/base_listings.html',c)


def search_listings(request):
    if ie_test(request):
        return fuck_ie(request)
    
    if not request.GET: # If not a get request
        return HttpResponseRedirect('/browse/') # Redirect

    latest_listing_list = Posting.objects.all().order_by('-date_modified')
    form = ViewForm(request.GET) # A form bound to the POST data

    try:
        if form.data['inc_inactive'] == 'on':
            latest_listing_list = Posting.objects.all().order_by('-date_modified')
    except:
        latest_listing_list = Posting.objects.all().order_by('-date_modified').filter(is_active=True)

    if form.data['med_center']:
        med_cent = form.data['med_center']
        latest_listing_list = latest_listing_list.filter(med_center=med_cent)

    if form.data['specialty']:
        spec = form.data['specialty']
        latest_listing_list = latest_listing_list.filter(specialty=spec)

    paginator = Paginator(latest_listing_list, 5)

    page = request.GET.get('page')
    try:
        latest_listing_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first
        # page.
        latest_listing_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range
        # (e.g. 9999), deliver
        # last page of results.
        latest_listing_list = paginator.page(paginator.num_pages)
    
    c = {
        'pagetitle': 'browse',
        'form': form,
        'latest_listings': latest_listing_list,
        }

    if not request.is_ajax():
        return render(request, 'agora/base_listings_inf.html',c)
    
    return render(request, 'agora/base_listings.html',c)


def detail(request, encrypted_id):
    if ie_test(request):
        return fuck_ie(request)
    
    now = datetime.now()
    post_id = unencrypt(encrypted_id)

    if not Posting.objects.get(id=post_id).is_alive:
        raise Http404

    if request.method == 'POST': # If the form has been submitted...
        reply_form = ReplyForm(request.POST) # A form bound to the POST data
        if reply_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ... here is where we save()
            try:
                if request.session['reply_time']:
                    return HttpResponseRedirect('/sorry/')
            except:                
                pass
            request.session['reply_time'] = True
            request.session.set_expiry(timedelta(seconds=60))
            reply = reply_form.save(commit=False)
            reply.posting_id = post_id
            reply.save()
            reply_post = Posting.objects.get(id=post_id)
            reply_post.number_replies += 1
            reply_post.save()
            subject = "re: %s" % (reply_post.title)
            message = reply.msg_body
            from_email = "projectMed <admin@projectMed.org>"
            to_email = reply_post.contact_email
            reply_header = {'Reply-To': "%s <%s>" % (reply.name, reply.contact_email)}
            email = EmailMessage(subject,message,from_email,[to_email], headers = reply_header)
            email.send(fail_silently=True)
            return HttpResponseRedirect('/reply_success/') # Redirect after POST
        else:
            owner_form = OwnerForm()
    else:
        reply_form = ReplyForm() # An unbound form
        owner_form = OwnerForm()

    post = Posting.objects.get(id=post_id)
        
    return render(request, 'agora/base_listing.html', {
        'listing': post,
        'form': reply_form,
        'owner_form' : owner_form,
        'pagetitle': 'listing',
    })


def mod_list(request, encrypted_id):
    if ie_test(request):
        return fuck_ie(request)
    
    post_id = unencrypt(encrypted_id)

    if request.method == "POST":
        owner_form = OwnerForm(request.POST)
        if owner_form.is_valid(): # All validation rules pass
            user_email = owner_form.cleaned_data['email']
            user_passkey = owner_form.cleaned_data['passkey']
            post = Posting.objects.get(id=post_id)
            if ((user_email == post.contact_email) and (user_passkey == post.passkey)):
                if 'edit_sub' in request.POST:
                    request.session['user'] = user_email
                    request.session['passkey'] = user_passkey
                    request.session.set_expiry(0)
                    return HttpResponseRedirect('/edit_project/%sL' %(encrypted_id))
                elif 'delete_sub' in request.POST:
                    post.is_alive = False
                    post.save()
                    return HttpResponseRedirect('/delete_success/')
            # incorrect user data
            else:
                return HttpResponseRedirect('/listings/%sL/#openModal' % (encrypted_id))
        # invalid form
        else:
            return HttpResponseRedirect('/listings/%sL/#openModal' % (encrypted_id))
            #raise Http404
    # not a post method
    else:
        return HttpResponseRedirect('/listings/%sL/#openModal' % (encrypted_id))


def post_project(request):
    if ie_test(request):
        return fuck_ie(request)
    
    now = datetime.now()
    if request.method == 'POST': # If the form has been submitted...
        form = PostingForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ... here is where we save()
            post = form.save()
            post.passkey = post.gen_passkey()
            post.date_modified = now
            post.save()
            # For email stuffs
            first_name = post.name.split()[0]
            subject = "projectMed: %s, save this email!" % (first_name)
            message = "Thank you for using projectMed, %s!\n\n\nWe\'ve added your listing:\n\"%s\"\n\nBelow is the permanent link to your project listing:\nhttp://www.projectMed.org/listings/%s/\n\nIf you need to edit/delete your project listing, you'll need this passkey:\n%s\n\n\nGood luck finding a great student collaborator,\nprojectMed Team" % (first_name,post.title,post.gen_url(),post.passkey)
            from_email = 'projectMed <admin@projectmed.org>'
            to_email = form.cleaned_data['contact_email']
            send_mail(subject, message, from_email, [to_email], fail_silently=True)
            return HttpResponseRedirect('/submit_success/') # Redirect after POST
    else:
        form = PostingForm() # An unbound form

    return render(request, 'agora/base_post_project.html', {
        'form': form,
        'pagetitle' : 'submit',
    })

def edit_project(request, encrypted_id):
    if ie_test(request):
        return fuck_ie(request)
    
    now = datetime.now()
    post_id = unencrypt(encrypted_id)
    post = Posting.objects.get(id=post_id)

    try:
        if not ((request.session['user'] == post.contact_email) \
            and (request.session['passkey'] == post.passkey)):
            pass
    # user needs to put in email and passkey
    except:
        return HttpResponseRedirect('/listings/%sL/#openModal' % (encrypted_id))
    
    if request.method == 'POST': # If the form has been submitted...
        form = PostingForm(data=request.POST, instance=post)
        if form.is_valid(): # All validation rules pass
            edit_post = form.save()
            edit_post.date_modified = now
            edit_post.save()
            return HttpResponseRedirect('/edit_success/') # Redirect after POST
    else:
        form = PostingForm(instance=post) # A form bound to the POST data
        
    return render(request, 'agora/base_edit_project.html', {
        'form' : form,
        'listing' : post,
        'pagetitle' : 'edit post',
    })


def about(request):
    if ie_test(request):
        return fuck_ie(request)
    
    t = loader.get_template('agora/base_text.html')
    about_text = open('static/misc/about.html','r')
    #about_text = open('/srv/www/projectmed.org/static/misc/about.html','r')
    text = about_text.read()
    c = Context({
        'pagetitle': 'about',
        'text': text,
        })
    return HttpResponse(t.render(c))


def contact(request):
    if ie_test(request):
        return fuck_ie(request)

    t = loader.get_template('agora/base_text.html')
    contact_text = open('static/misc/contact.html','r')
    #contact_text = open('/srv/www/projectmed.org/static/misc/contact.html','r')
    text = contact_text.read()
    c = Context({
        'pagetitle': 'contact',
        'text': text,
        })
    return HttpResponse(t.render(c))


def terms(request):
    if ie_test(request):
        return fuck_ie(request)

    t = loader.get_template('agora/base_text.html')
    terms_text = open('static/misc/terms.html','r')
    #terms_text = open('/srv/www/projectmed.org/static/misc/terms.html','r')
    text = terms_text.read()
    c = Context({
        'pagetitle': 'terms',
        'text': text,
        })
    return HttpResponse(t.render(c))


def submission_success(request):
    t = loader.get_template('agora/base_success.html')
    c = Context({
        'pagetitle': 'success',
        'text': 'Thank you for using projectMed. Your submission was \
        successfully received!\nPlease check your email for permalink \
        and passkey in case you ever need to edit or delete your listing.',
        'redirect': 'listings',
        })
    return HttpResponse(t.render(c))


def reply_success(request):
    t = loader.get_template('agora/base_success.html')
    c = Context({
        'pagetitle': 'success',
        'text': 'Thank you for using projectMed. Your reply was \
        successfully received!',
        'redirect':'close',
        })
    return HttpResponse(t.render(c))


def delete_success(request):
    t = loader.get_template('agora/base_success.html')
    c = Context({
        'pagetitle': 'success',
        'text': 'Thank you for using projectMed. Your listing was \
        successfully deleted.',
        'redirect':'listings',
        })
    return HttpResponse(t.render(c))


def edit_success(request):
    t = loader.get_template('agora/base_success.html')
    c = Context({
        'pagetitle': 'success',
        'text': 'Thank you for using projectMed. Your listing was \
        successfully edited!',
        'redirect':'listings',
        })
    return HttpResponse(t.render(c))


def one_per_minute(request):
    t = loader.get_template('agora/base_success.html')
    c = Context({
        'pagetitle': 'sorry',
        'text': 'Sorry. You may only reply once per minute.',
        'redirect': 'none',
        })
    return HttpResponse(t.render(c))


def unencrypt(encrypted_id):
    cipher = 0xabcdef
    encrypted = int(encrypted_id,16)
    pid = encrypted ^ cipher
    return pid


def coming_soon(request):
    t = loader.get_template('agora/base_comingsoon.html')
    c = Context({
        'pagetitle': 'coming soon',
        })
    return HttpResponse(t.render(c))


def maintenance(request):
    if ie_test(request):
        return fuck_ie(request)

    t = loader.get_template('agora/base_text.html')
    c = Context({
        'pagetitle': 'maintenance',
        'text': 'Temporarily down for maintenance. Please come back in a few minutes!'
        })
    return HttpResponse(t.render(c))


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

