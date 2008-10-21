from django.shortcuts import render_to_response
from django import forms
from haydle.search.models import SearchForm
import twitter
import classify
import time

def search(str):
    api = twitter.Api()
    data = api.Search(str)
    # now we have bag of twitter.Status examples
    # return [x.text for x in data]
    return data



def index(request,query=''): 
    results = {}
    resultsgood = None
    resultsbad = None
    search_terms = ''
    numpos = 0
    numneg = 0
    numneu = 0
    if query != '':
       search_terms = query
       form = SearchForm(initial={'search_terms': query})
    if request.method == "POST":
       form = SearchForm(request.POST)
       if form.is_valid():
          search_terms = form.cleaned_data['search_terms']

    if search_terms != '': 

          results = search(search_terms)
	  print "Search done"
	  time.sleep(0.1)
          resultsgood = search(search_terms + ' :)')
	  print "Good search done"
	  time.sleep(0.1)
          resultsbad = search(search_terms + ' :(')
	  print "Bad search done"

          cl = classify.naivebayes(classify.getwords)
          for r in resultsbad:
              cl.train(r.text, 'bad')
          for r in resultsgood:
              cl.train(r.text, 'good')
 
          cl.setthreshold('good',1.2)
          cl.setthreshold('bad',1.5)

          # gooddist = [] 
	  # baddist = []


          for r in results:
              r.probgood = cl.prob(r.text,'good')
	    #  gooddist.append(r.probgood)
              r.probbad  = cl.prob(r.text,'bad')
	    #  baddist.append(r.probbad)
              r.polarity = cl.classify(r.text, default='neutral')
	      if (r.polarity == 'good'):
	         numpos+=1
	         r.rgbr = 255
		 r.rgbb = 190
	      elif (r.polarity == 'bad'):
	         numneg+=1
	         r.rgbr = 190
		 r.rgbb = 255
	      else: 
	         numneu+=1
	         r.rgbr = 190
		 r.rgbb = 190
             # if (r.polarity == 'neutral'):
             #    results.del(r) 

          # Normalise to 255
	  # Normalisation doesn't work, range too large with small value-set.
	  # gooddist.sort()
	  # baddist.sort()
	  # goodalpha = 255 / gooddist[int(len(gooddist)*.75)]
	  # badalpha = 255 / baddist[int(len(baddist)*.75)]

          # must be a less clunky way than this?
	  # javascript function? :/

	  # for r in results:
	  #     r.rgbr = r.probgood * goodalpha
	  #     print r.rgbr
	  #     r.rgbb = int(r.probbad * badalpha)

    else:
       form = SearchForm()
    return render_to_response('search/index.html', {'form': form, 'results': results, 'numpos':numpos, 'numneg':numneg,'numneu':numneu, })
