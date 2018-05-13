import math, collections

class StupidBackoffLanguageModel:

  def __init__(self, corpus):
    self.unigramCounts = collections.defaultdict(lambda:0)
    self.bigramCounts = collections.defaultdict(lambda:0)
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    for sentence in corpus.readlines():
        token1 = ''
        token2 = ''
        words = sentence.split()
	for word in words:
	    token2 = word
	    self.total += 1
	    self.bigramCounts[(token1,token2)] = self.bigramCounts[(token1,token2)]+1
	    self.unigramCounts[token2] = self.unigramCounts[token2] + 1
	    token1 = word
    # pass


  def score(self, sentence):
    score = 0.0
    token1 = '<s>'
    token2 = ''
    for word in sentence:
	token2 = word
	count = self.bigramCounts[(token1,token2)]
	if count > 0:
	    score += math.log(count)
	    score -= math.log(self.unigramCounts[token1])
	else:
	    score += math.log(0.4) + math.log(self.unigramCounts[token2]+1)
	    score -= math.log(self.total + (len(self.unigramCounts)))
	token1 = word
    token2 = '</s>'
    count = self.bigramCounts[(token1,token2)]
    if count > 0:
	score += math.log(count)
	score -= math.log(self.unigramCounts[token1])
    else:
	score += math.log(0.4) + math.log(self.unigramCounts[token2]+1)
	score -= math.log(self.total + (len(self.unigramCounts)))


    return score