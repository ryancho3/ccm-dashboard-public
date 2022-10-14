from queue import Empty
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import httpagentparser

from django.contrib.auth.models import User
from .models import Campaign, School, Impression
from .utils import register_check, register_manager_from_post, get_school_impressions



class IndexView(generic.ListView):
    template_name = 'campaigns/index.html'
    context_object_name = 'latest_campaign_list'

    def get_queryset(self):
        return Campaign.objects.order_by('-start_date')[:5]

@require_http_methods(["GET"])
@login_required
def campaign_detail(request, campaign_code):
    campaign = get_object_or_404(Campaign, pk=campaign_code)
    impressions = Impression.objects.filter(campaign=campaign).order_by('datetime')
    total_impressions = impressions.count()
    recent_impressions = impressions[0:10]
    school_impressions, school_recent_impressions = get_school_impressions(request.user, campaign)
    return render(request, 'campaigns/campaign.html', {'user': request.user, 
                                                    'campaign': campaign,
                                                    'total_impressions': total_impressions,
                                                    'recent_impressions': recent_impressions,
                                                    'school_impressions': school_impressions,
                                                    'school_recent_impressions': school_recent_impressions})

@require_http_methods(["GET"])
def count_then_redirect(request, campaign_code, school_code):
    campaign = get_object_or_404(Campaign, pk=campaign_code)
    school = get_object_or_404(School, pk=school_code)
    impression = Impression(campaign=campaign, school=school)
    
    os = httpagentparser.detect(request.META["HTTP_USER_AGENT"])['platform']['name']
    if os == 'iOS':
        if campaign.link_ios is not Empty:
            impression.save()
            return redirect(campaign.link_ios)
        else:
            return HttpResponse("This app doesn't have an iOS version yet.")
    elif os == 'Android':
        if campaign.link_android is not Empty:
            impression.save()
            return redirect(campaign.link_android)
        else:
            return HttpResponse("This app doesn't have an Android version yet.")
    
    return HttpResponse("You need to acccess this site from a mobile device.")

@require_http_methods(["GET", "POST"])
def user_register(request):
    school_list = School.objects.all()
    if request.method == "POST":
        post = request.POST
        print(post)
        if register_check(post) == "valid":
            user = register_manager_from_post(post)
            login(request, user)
            return render(request, 'campaigns/user_register_success.html')
        else:
            return render(request, 'campaigns/user_register.html', {'error': register_check(post),
                                                                    'school_list': school_list})
    
    return render(request, 'campaigns/user_register.html', {'school_list': school_list})

@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'campaigns/user_login.html', {'user': request.user,
                                                                'error': 'Invalid username or password.'})

    return render(request, 'campaigns/user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'campaigns/user_login.html', {'user': request.user, 
                                                        'error': 'Successfully Logged Out.'})

@login_required
def user_profile(request):
    user = request.user
    if not user.is_staff and not user.is_superuser:
        school_list = user.manager.school.all()
    else:
        school_list = None
    return render(request, 'campaigns/profile.html', {'user': user,
                                                    'school_list': school_list})