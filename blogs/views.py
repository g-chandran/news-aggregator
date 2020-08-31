from django.views.generic import TemplateView, ListView
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views import generic 
from .models import Subscription, Article
from django.http import HttpResponseRedirect
from django.shortcuts import render
import feedparser as fp
from bs4 import BeautifulSoup

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
  subscriptions = Subscription.objects.all()
  for i in subscriptions:
    feed = fp.parse(i.feed_link)
    if feed.entries[0].published != i.last_updated:
      i.last_updated = feed.entries[0].published
      i.save()
      print('Updating ' + str(i.name))
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
          a = Article.objects.create(subscription_name=i, published=pubTime, title=title, author=author, summary=summary, media=media, article_id=iD, article_link=link)
          a.save()
    print(f"{i.name} done")
            # print(f"{i.name}\nPublished at: {pubTime}\nTitle: {title}\nLink: {link}\nID: {iD}\nAuthor: {author}\nSummary: {summary}\nMedia Link: {media}\n")
  print('Completed!')
  return render(request, 'aggregator.html')

def homeListView(request):
  allData = Article.objects.order_by('-id')
  paginator = Paginator(allData, 5)  # Show 25 contacts per page.
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  return render(request, 'home.html', {'allData': page_obj})

class HomeListView(ListView):
    model = Article
    template_name = "home.html"
    ordering = ['-id']
    paginate_by = 5
    context_object_name = 'allData'
