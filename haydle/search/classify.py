import re
import math

# Now the fun bit. Building a classifier
# Baseline from Prog. Collective Intelligence pg188pp

def getwords(sent):
    splitter = re.compile('\\W*')
    # Split by non-alpha
    words = [s.lower() for s in splitter.split(sent) if len(s)>2 and len(s)<20]
    # Return (Lets not do uniques for now)
    return words

class classifier:
     def __init__(self,getfeatures,filename=None):
       # counts of feature/categories
       self.fc = {}
       # counts of examples in each cat
       self.cc = {}
       self.getfeatures = getfeatures
     
     # Methods to alter and access counts.
    
     # increase feature,cat pair count 
     def incf(self,f,cat):
        self.fc.setdefault(f,{})
        self.fc[f].setdefault(cat,0)
        self.fc[f][cat] += 1

     # increase cat count
     def incc(self,cat):
        self.cc.setdefault(cat,0)
        self.cc[cat] += 1

     # Number of times feature appears in cat
     def fcount(self,f,cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

     # Number of items in cat
     def catcount(self,cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0.0

     # Total number of items
     def totalcount(self):
         return sum(self.cc.values())
    
     # Category list
     def categories(self):
         return self.cc.keys()

     # Train method for supervised examples
     def train(self,item,cat):
         features = self.getfeatures(item)
         # For every feature in this item, increment count for this category
         for f in features:
             self.incf(f,cat)
         # Then increment count of category (total examples in cat)
         self.incc(cat)

     # Get probability of feature being in category
     def fprob(self,f,cat):
        if self.catcount(cat) == 0: return 0
        # p (f,cat) = num(f,cat)/num(cat)
        return self.fcount(f,cat)/self.catcount(cat)

     # weight probabilities so extremes do not skew influence
     def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
        # Current prob
        basicprob = prf(f,cat)
        
        # How many instances of the feature have we seen
        totals=sum([self.fcount(f,c) for c in self.categories()])
  
        # Weighted avg
        bp = ((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp
     

# Create a Naive Bayes classifier that uses the bag of words weighted probabilities to classify a sentence.

class naivebayes(classifier):

    def __init__(self,getfeatures):
       classifier.__init__(self,getfeatures)
       self.thresholds = {}

    def docprob(self,item,cat):
       features = self.getfeatures(item)

       # Multiply probabilities of all the features = P (Doc | Cat)
       p = 1
       for f in features: p*=self.weightedprob(f,cat,self.fprob)
       return p
  
    def prob(self,item,cat):
       # Bayes: P (Cat | Doc) = P (Doc|Cat) * P(Cat) / P(Doc)
       catprob = self.catcount(cat)/self.totalcount()
       docprob = self.docprob(item,cat)
       return docprob * catprob

    # Adding in threshold for categories
    def setthreshold(self,cat,t):
       self.thresholds[cat]=t

    def getthreshold(self,cat):
       if cat not in self.thresholds: return 1.0
       return self.thresholds[cat]

    def classify(self,item,default=None):
       probs = {}
       # Find cat with highest pr
       max = 0.0
       for cat in self.categories():
         probs[cat]=self.prob(item,cat)
         if probs[cat]>max:
            max = probs[cat]
            best = cat
       
       # Make sure cat > threshold*next best
       for cat in probs:
          if cat==best: continue
          if probs[cat]*self.getthreshold(best)>probs[best]: return default
   
       return best   
