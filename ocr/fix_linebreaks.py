#remove empty lines and fix line breaks

import sys

 
rawlines_path = sys.argv[1]



with open(rawlines_path) as f:
    rawlines = f.readlines()

rawlines = [x.strip() for x in rawlines if len(x.strip())>0]


prepend_word=False
next_word="+++++"


#lines=[]


for l in rawlines:
	new_line=l
	splited_l=new_line.split(" ")
	if prepend_word:
		splited_l[0]=next_word+splited_l[0]
	prepend_word=False
	if len(splited_l)>1 and splited_l[-1][-1]=="-":
		last_word=splited_l[-1]
		next_word=last_word[0:-1]
		prepend_word=True
		splited_l = splited_l[0:-1]
	new_line=" ".join(splited_l)
	print (new_line)
	#lines.append(new_line)


