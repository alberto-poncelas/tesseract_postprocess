import sys
import ConfigParser
import difflib
import string
import nltk
from nltk.corpus import words
choices = words.words()



#File for processing the text as follows (recognize implies that it exists in a vocabulary):
#if a word is recognized (but contain ambig chars) --> replace ambig chars and add them as alternative
#if a word is not recognized --> split the word AND/OR get closer words




config = ConfigParser.ConfigParser()
config.readfp(open(r'../config'))
vocabulary_file = config.get('DEFAULT', 'VOCAB')
ambig_chars_file = config.get('DEFAULT', 'AMBIG_CHARS')




input_file = sys.argv[1]




with open(input_file) as fin:
    data = fin.readlines()




##Get vocabulary
with open(vocabulary_file) as f:
    wordlist_tr_pre = f.readlines()

wordlist_tr = [x.strip().lower() for x in wordlist_tr_pre]
choices= set(wordlist_tr + words.words() + list(string.punctuation))



#Get ambig characters
with open(ambig_chars_file) as famb:
    ambi_chars_file = famb.readlines()
ambig_chars=dict([x.strip().split("\t") for x in ambi_chars_file])






def has_ambig_char(w):
	return len(set(w.lower()).intersection(ambig_chars.keys()))>0


def is_unrecognized(w):
	return w.lower() not in set(choices)




def replace_ambig(w):
	listw=list(w)
	altern=[]
	for i in range(0,len(listw)):
		current_char=listw[i]
		if current_char in ambig_chars.keys():
			new_word=list(w)
			new_word[i]=ambig_chars[current_char]
			new_word="".join(new_word)
			if not is_unrecognized(new_word):
				altern.append(new_word)
	return set(altern)


#get similar existing words
def get_close_matches(w):
	return set(difflib.get_close_matches(w.lower(), choices,3))


#split words that may be joined
def split_word(w):
	altern=[]
	for i in range(1,len(w)-1):
		w1 = w[0:i]
		w2 = w[i:len(w)]
		if (w1.lower() in choices) and (w2.lower() in choices):
			splited_w = w1+" "+w2
			altern.append( splited_w )
	return set(altern)




##
##Get Alternatives
def get_altern(w):
	altern=set()
	if has_ambig_char(w):
		altern=altern.union(replace_ambig(w))
	if is_unrecognized(w):
		altern=altern.union(get_close_matches(w))
		altern=altern.union(split_word(w))
	return set(altern)




##Process text and retrieve the dictionary of possible replacements
flatten = lambda l: [item for sublist in l for item in sublist]
vocab = set(flatten([nltk.word_tokenize(s.lower()) for s in data]))
for w in vocab:
	altern=list(get_altern(w))
	if len(altern)>0:
		print(str(w)+"->"+str(altern))


