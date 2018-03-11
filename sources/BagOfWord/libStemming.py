from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

arrV ='ueoai'

def countVC(word): #[C](VC){m}[V]
	if not word:
		return 0
	inum = 0
	count = 0
	leng = len(word)
	while inum<leng-1:
		if word[inum] in arrV: # if is V*
			if word[inum+1] not in arrV: # is VC
				count = count + 1
				inum = inum + 2
			else: # is VV
				inum = inum + 1
		else:
			inum = inum + 1
	return count

def v(word): #the stem contains a vowel.
	if not word:
		return False
	inum = 0
	leng = len(word)
	count = 0
	while inum<leng:
		if word[inum] in arrV:
			return True
		inum = inum+1
	return False

def d(word): #the stem ends with a double consonant (e.g. -TT, -SS).
	if not word:
		return False
	leng = len(word)
	if (word[leng-1] == word[leng-2]) and (word[leng-1] not in arrV):
		return True
	return False

def o(word): #the stem ends cvc, where the second c is not W, X or Y (e.g. -WIL, -HOP).
	if not word:
		return False
	leng = len(word)
	if (word[leng-1] not in arrV) and (word[leng-1] not in 'wxy') and (word[leng-2] in arrV) and (word[leng-3] not in arrV):
		return True
	return False

def step1(word):
	leng = len(word)
	#a
	if word.endswith('sses'):
		word = word[:-2]
	elif word.endswith('ies'):
		word = word[:-2]
	elif word.endswith('ss'):
		word = word
	elif word.endswith('s'):
		word = word[:-1]
	#b

	if countVC(word[:-3])>0 and word.endswith('eed'): # something wrong when I test with agreed -> agree but result when wrong
		word = word[:-1]
	elif word.endswith('eed'):
		word = word
	elif (v(word[:-2]) and word.endswith('ed')) or (v(word[:-3]) and word.endswith('ing')):
		if word.endswith('ed'):
			word = word[:-2]
		elif word.endswith('ing'):
			word = word[:-3]
		leng = len(word)

		if word.endswith('at') or word.endswith('bl') or word.endswith('iz'):
			word =  word+'e'
		elif d(word) and (word[leng-1] not in 'lsz'):
			word =  word[:-1]

	if v(word[:-1]) and word.endswith('y'):
		word = word[:-1]+'i'
	return word

def step2(word):
	if word.endswith('ational') and countVC(word[:-7]) > 0:
		return word[:-5]+'e'
	elif word.endswith('tional') and countVC(word[:-6]) > 0:
		return word[:-2]
	elif word.endswith('enci') and countVC(word[:-4]) > 0:
		return word[:-1]+'e'
	elif word.endswith('anci') and countVC(word[:-4]) > 0:
		return word[:-1]+'e'
	elif word.endswith('izer') and countVC(word[:-4]) > 0:
		return word[:-1]
	elif word.endswith('abli') and countVC(word[:-4]) > 0:
		return word[:-1]+'e'
	elif word.endswith('alli') and countVC(word[:-4]) > 0:
		return word[:-2]
	elif word.endswith('entli') and countVC(word[:-5]) > 0:
		return word[:-2]
	elif word.endswith('eli') and countVC(word[:-3]) > 0:
		return word[:-2]
	elif word.endswith('ousli') and countVC(word[:-5]) > 0:
		return word[:-2]
	elif word.endswith('ization') and countVC(word[:-7]) > 0:
		return word[:-5]+'e'
	elif word.endswith('ation') and countVC(word[:-5]) > 0:
		return word[:-3]+'e'
	elif word.endswith('ator') and countVC(word[:-4]) > 0:
		return word[:-2]+'e'
	elif word.endswith('alism') and countVC(word[:-5]) > 0:
		return word[:-3]
	elif word.endswith('iveness') and countVC(word[:-7]) > 0:
		return word[:-4]
	elif word.endswith('fulness') and countVC(word[:-7]) > 0:
		return word[:-4]
	elif word.endswith('ousness') and countVC(word[:-7]) > 0:
		return word[:-4]
	elif word.endswith('aliti') and countVC(word[:-5]) > 0:
		return word[:-3]
	elif word.endswith('iviti') and countVC(word[:-5]) > 0:
		return word[:-3]+'e'
	elif word.endswith('biliti') and countVC(word[:-6]) > 0:
		return word[:-4]+'e'
	return word

def step3(word):

	if word.endswith('icate') and countVC(word[:-5]) > 0:
		return word[:-3]
	elif word.endswith('ative') and countVC(word[:-5]) > 0:
		return word[:-5]
	elif word.endswith('alize') and countVC(word[:-5]) > 0:
		return word[:-3]
	elif word.endswith('iciti') and countVC(word[:-5]) > 0:
		return word[:-3]
	elif word.endswith('ical') and countVC(word[:-4]) > 0:
		return word[:-2]
	elif word.endswith('ful') and countVC(word[:-3]) > 0:
		return word[:-3]
	elif word.endswith('ness') and countVC(word[:-4]) > 0:
		return word[:-4]
	return word

def step4(word):
	if word.endswith('al') and countVC(word[:-2]) > 1:
		return word[:-2]
	elif word.endswith('ance') and countVC(word[:-4]) > 1:
		return word[:-4]
	elif word.endswith('ence') and countVC(word[:-4]) > 1:
		return word[:-4]
	elif word.endswith('er') and countVC(word[:-2]) > 1:
		return word[:-2]
	elif word.endswith('ic') and countVC(word[:-2]) > 1:
		return word[:-2]
	elif word.endswith('able') and countVC(word[:-4]) > 1:
		return word[:-4]
	elif word.endswith('ible') and countVC(word[:-4]) > 1:
		return word[:-4]
	elif word.endswith('ant') and countVC(word[:-3]) > 1:
		return word[:-3]
	elif word.endswith('ement') and countVC(word[:-5]) > 1:
		return word[:-5]
	elif word.endswith('ment') and countVC(word[:-4]) > 1:
		return word[:-4]
	elif word.endswith('ent') and countVC(word[:-3]) > 1:
		return word[:-3]
	elif word.endswith('ion') and (word[-4] in 'st') and countVC(word[:-3]) > 1:
		return word[:-3]
	elif word.endswith('ou') and countVC(word[:-2]) > 1:
		return word[:-2]
	elif word.endswith('ism') and countVC(word[:-3]) > 1:
		return word[:-3]
	elif word.endswith('ate') and countVC(word[:-3]) > 1:
		return word[:-3]
	elif word.endswith('iti') and countVC(word[:-3]) > 1:
		return word[:-3]
	elif word.endswith('ous') and countVC(word[:-3]) > 1:
		return word[:-3]
	elif word.endswith('ive') and countVC(word[:-3]) > 1:
		return word[:-3]
	elif word.endswith('ize') and countVC(word[:-3]) > 1:
		return word[:-3]
	return word

def step5(word):
	#a
	if countVC(word[:-1]) > 1 and word.endswith('e'):
		word = word[:-1]
	elif (countVC(word[:-1]) == 1 ) and not o(word[:-1]) and word.endswith('e'):
		word = word[:-1]
	#b
	if (countVC(word[:-2])>1) and d(word) and word.endswith('l'):
		word = word[:-1]
	return word


def stemming(word):
	#special
	special = ['is','as']
	if word in special:
		return word
	#print ('0', word)
	stemmed_word = step1(word)
	#print ('1', stemmed_word)
	stemmed_word = step2(stemmed_word)
	#print ('2', stemmed_word)
	stemmed_word = step3(stemmed_word)
	#print ('3', stemmed_word)
	stemmed_word = step4(stemmed_word)
	#print ('4', stemmed_word)
	stemmed_word = step5(stemmed_word)

	#print (word, stemmed_word)
	return stemmed_word
