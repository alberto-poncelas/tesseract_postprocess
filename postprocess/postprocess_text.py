
import sys
import string
import nltk
import ConfigParser



import io



config = ConfigParser.ConfigParser()
config.readfp(open(r'../config'))
language_model_path = config.get('DEFAULT', 'LM')



input_data = sys.argv[1]
replacement_dict_path = sys.argv[2]




with io.open(input_data,"r", encoding="utf-8") as finp:
    data = finp.readlines()



from nltk.tokenize.treebank import TreebankWordDetokenizer
detok=TreebankWordDetokenizer()



#Get Language Model
import kenlm
LMmodel = kenlm.Model(language_model_path)






##Get replacement dict
with io.open(replacement_dict_path,"r", encoding="utf-8") as frep:
    alternative_dict_text = frep.readlines()


alternative_elems=[x.strip().split("->") for x in alternative_dict_text]

alternative_dict=dict()
for elem in alternative_elems:
	#remove "[" and "]", then split
	values=elem[1][2:-2].split("', '")
	alternative_dict[elem[0]]=values

unrecognized_words_list=alternative_dict.keys()







#replace the i-th word in the sentence (as list) with the word w
def replace_word_list(listS,i,w):
	new_sentence=list(listS)
	new_sentence[i]=w
	return new_sentence



#Return w2, with the same case as w1
def same_case(w,w2):
	if w.isupper():
		return w2.upper()
	elif w[0].isupper():
		return w2.capitalize()
	else:
		return w2



#Get the alternative sentences for the word i
def candidate_sentences_i(listS,i):
	alternative_sentences=[listS]
	replacements=[ [] ]
	w_orig=listS[i]
	w=w_orig.lower()
	if w in unrecognized_words_list:
		altern=alternative_dict[w]
		for alt_lower in altern:
			alt=same_case(w_orig,alt_lower) #Same case as the original word
			alternative_sentences.append(replace_word_list(listS,i,alt))
			replacements.append([w_orig,alt])
	return alternative_sentences , replacements



#score a sentence (list of words) according to the LM
def sentence_score(listS):
	return LMmodel.score(" ".join(listS).lower())


#get the best candidate according to the LM
def postproc_sentence(s):
	listS=list(s.strip().split(" "))
	replacements_list=[]
	for i in range(0,len(listS)):
		candidates ,replacements = candidate_sentences_i(listS,i)
		scores=[sentence_score(x) for x in candidates]
		best_sentence_idx=scores.index(max(scores))
		#Replace the sentence with the best candidate
		listS = candidates[best_sentence_idx]
		replacements_list.append(replacements[best_sentence_idx] )
	#return " ".join(listS),replacements_list
	return detok.detokenize(listS),replacements_list







#Print postprocessed sentence (and the dictionaries of replacements done)
def format_replacements_list(replac_list):
	replac_list_out=[]
	for x in replac_list:
		if len(x)>0:
			replac_list_out.append(x[0]+"->"+x[1])
	return "; ".join(replac_list_out)


for s in data:
	post_sent , replac = postproc_sentence(s)
	replac_str=format_replacements_list(replac)
	print( (post_sent+"\t"+replac_str).encode("UTF8") )


