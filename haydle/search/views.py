from django.shortcuts import render_to_response
from django import forms
from haydle.search.models import SearchForm
import twitter
import classify

def search(str):
    api = twitter.Api()
    data = api.Search(str)
    # now we have bag of twitter.Status examples
    # return [x.text for x in data]
    return data

def index(request): 
    results = None
    resultsgood = None
    resultsbad = None
    if request.method == "POST":
       form = SearchForm(request.POST)
       if form.is_valid():
          search_terms = form.cleaned_data['search_terms']
          results = search(search_terms)
          resultsgood = search(search_terms + ' :)')
          resultsbad = search(search_terms + ' :(')

          cl = classify.naivebayes(classify.getwords)
          for r in resultsbad:
              cl.train(r.text, 'bad')
          for r in resultsgood:
              cl.train(r.text, 'good')
 
          cl.setthreshold('good',1)
          cl.setthreshold('bad',2)
          for r in results:
              r.probgood = cl.prob(r.text,'good')
              r.probbad  = cl.prob(r.text,'bad')
              r.polarity = cl.classify(r.text, default='neutral')

    else:
       form = SearchForm()
    return render_to_response('search/index.html', {'form': form, 'results': results, 'resultsgood': resultsgood, 'resultsbad': resultsbad})
