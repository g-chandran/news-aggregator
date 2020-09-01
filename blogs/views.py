from django.views.generic import TemplateView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views import generic 
from .models import Subscription, Article
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import feedparser as fp
from bs4 import BeautifulSoup
from dateutil.parser import parse as p
import datetime as dt
import pytz

class HomePageView(TemplateView):
  template_name = "home.html"

class SignupView(generic.CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('home')
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
          a = Article.objects.create(subscription_name=i, published=p(pubTime), title=title, author=author, summary=summary, media=media, article_id=iD, article_link=link)
          a.save()
    print(f"{i.name} done")
  print('Completed!')
  current_time = dt.datetime.now(pytz.timezone('UTC'))
  indian_time = current_time.astimezone(pytz.timezone('Asia/Kolkata'))
  return render(request, 'aggregator.html', {'now': indian_time, 'month': indian_time.strftime("%B"), 'updateList': updateList})

def homeListView(request):
  allData = Article.objects.order_by('-id')
  paginator = Paginator(allData, 5)  # Show 25 contacts per page.
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  return render(request, 'home.html', {'allData': page_obj})

class HomeListView(ListView):
    model = Article
    template_name = "home.html"
    ordering = ['-published']
    paginate_by = 20
    context_object_name = 'allData'

class SubscriptionListView(ListView):
  model = Article
  template_name = 'subscription.html'
  paginate_by = 20

  def get_queryset(self):
    article = get_object_or_404(Article, )
    queryResults = Article.objects.filter()
    return super().get_queryset()
