from libStemming import stemming

def BagOfWord(bag, text):
	#remove stop word
	newBag = [stemming(w.lower()) for w in text.split()]
	if len(newBag)>0:
		for word in newBag:
			if word in bag.keys():
				bag[word]=bag[word]+1
			else:
				bag[word]=1
	return bag
