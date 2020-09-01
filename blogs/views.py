from django.views.generic import TemplateView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views import generic 
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

import feedparser as fp
from bs4 import BeautifulSoup
from dateutil.parser import parse as p
import datetime as dt
import pytz

from .models import Subscription, Article, Profile

class HomePageView(TemplateView):
  template_name = "home.html"

class SignupView(generic.CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('login')
  template_name = 'signup.html'

def summaryMaker(originalText):
  if len(originalText) >= 400:
    return originalText[0: 395] + "..."
  return originalText

def aggregator(request):
  updateList = []
  subscriptions = Subscription.objects.all()
  for i in subscriptions:
    feed = fp.parse(i.feed_link)
    if p(feed.entries[0].published) != i.last_updated:
      i.last_updated = p(feed.entries[0].published)
      i.save()
      print('Updating ' + str(i.name))
      updateList.append(i.name)
      for j in feed.entries:
        if Article.objects.filter(article_id=j.id).count() == 0:
          pubTime = j.published
          title = j.title
          link = j.link
          iD = j.id
          summary = j.summary

          # Summary
          if i.name == 'Gizmo China' or i.name == 'GSM Arena':
            htmlToText = BeautifulSoup(summary, "html.parser")
            summary = htmlToText.text.split('\n')[0]
          summary = summaryMaker(summary)

          try:
            author = j.author
          except Exception as e:
            author = ' '

          try:
            media = j.media_content[0]['url']
          except Exception as e:
            try:
              media = j.links[1]['href']
            except Exception as e:
              try:
                media = htmlToText.find('img')['src']
              except Exception as e:
                media = i.thumbnail
          converted_time = p(pubTime).astimezone(pytz.timezone('Asia/KolKata'))
          a = Article.objects.create(subscription_name=i, published=converted_time, title=title, author=author, summary=summary, media=media, article_id=iD, article_link=link)
          a.save()
    print(f"{i.name} done")
  print('Completed!')
  current_time = dt.datetime.now(pytz.timezone('UTC'))
  indian_time = current_time.astimezone(pytz.timezone('Asia/Kolkata'))
  return render(request, 'aggregator.html', {'now': indian_time, 'updateList': updateList, 'month': indian_time.strftime("%B")})

class HomeListView(ListView):
  model = Article
  template_name = "home.html"
  paginate_by = 20
  context_object_name = 'allData'

  def get_queryset(self):
    if self.request.user.is_authenticated:
      subs = Profile.objects.filter(name=self.request.user)
      lister = []
      for sub in subs:
        lister.append(sub.subscription)
      return Article.objects.filter(subscription_name__in=lister).order_by('-published')
    else:
      return Article.objects.all().order_by('-published')

class SubscriptionListView(ListView):
  model = Article
  template_name = 'subscription.html'
  paginate_by = 20
  context_object_name = 'allData'
  
  def get_queryset(self):
    subs = get_object_or_404(Subscription, name=self.kwargs.get('name'))
    return Article.objects.filter(subscription_name=subs).order_by('-published')

@login_required
def profileView(request):
  allSubscriptions = Subscription.objects.all()
  profile = Profile.objects.filter(name=request.user)
  lister=[]
  for pr in  profile:
    lister.append(pr.subscription.name)
  context = {'subscriptions': allSubscriptions, 'profiles': lister}
  return render(request, 'profile.html', context)

@login_required
def addProfile(request, id):
  allSubscriptions = Subscription.objects.all()
  sub = get_object_or_404(Subscription, id=id)
  p = Profile.objects.create(name=request.user, subscription=sub)
  p.save()
  profile = Profile.objects.filter(name=request.user)
  lister = []
  for pr in profile:
    lister.append(pr.subscription.name)
  return render(request, 'profile.html', {'subscriptions': allSubscriptions, 'profiles': lister})

@login_required
def removeProfile(request, id):
  sub = get_object_or_404(Subscription, id=id)
  p=Profile.objects.filter(name=request.user, subscription=sub).delete()
  allSubscriptions = Subscription.objects.all()
  # p.delete()
  profile = Profile.objects.filter(name=request.user)
  lister = []
  for pr in profile:
    lister.append(pr.subscription.name)
  return render(request, 'profile.html', {'subscriptions': allSubscriptions, 'profiles': lister})
