

## Obtain PDF

The pdf of `Essay Towards Regulating the Trade.pdf` can be downloaded as:

```
PDF_URL="https://books.googleusercontent.com/books/content?req=AKW5Qae0v2jr0PpCHKswJxdUaswMKzxJrxRz1p0MWGjTP1j-7HUaOrGnXr0qU6r1PHXQ8RUQBGvpOWHCqBH6gxHPHIlKc-UpVelL-LYovPlnBFffYeYijylLCn107KjRUHmjB3N_Y4mPXWWZOs0KWPzajbx5UPjGyJegh9Am4AcfqyQnbmefkdmgHMy5Y4WO7ORC-H0GiRdjzXtf_Wre_xKv-raP2AsuE2QecClpSyw5NVCccE7JAnHg8VSjAjhte30vQdh8BJ4SMBMvOh8p5lWQZg5nfzh8kw"
wget -O An_Essay_Towards_Regulating_the_Trade.pdf $PDF_URL
```



## Get resources
In order to process the output of the OCR, a vocabulary list and a language model is required. We get 

Download books from Gutemberg project:
```
wget -w 2 -m -H "http://www.gutenberg.org/robot/harvest?langs[]=en&filetypes[]=txt"
```

We use `en` for getting the books in English. It is also possible to specify `ang` or `enm` for getting Ancient English and Middle English books.

The files will be stored in the `aleph.gutenberg.org` folder. We copy it into a `zips` folder ad extract them.

```
mkdir zips
cp aleph.gutenberg.org/*/*/*/*/*/*.zip zips

rm -r www.gutenberg.org
rm -r aleph.gutenberg.org
cd zips
mkdir books

files=$(ls *zip)
for z in $files; do 
    unzip $z -d books
done
cd ..
```

Combine all the files extracted and preprocess:
1. Remove multiple spaces
2. Apply lowercase
3. Tokenize the text

In order to do that we execute the following command:
```
cat zips/books/*.txt   \
 | sed 's/  */ /g' \
 | awk -F"\t" '{ if (length($0)>1) {print tolower($0)} }' \
 | awk '{print gensub(/\y[[:punct:]]/," \\0 ","g")}' > books.tok.txt
```

### Get vocabulary

The vocabulary file can be obtained by running:
```
grep -o -E '\w+' books.tok.txt | sort | uniq > vocabulary.txt
```
Additionally other resources can be use, such as [the data set from dwyl](https://github.com/dwyl/english-words/blob/master/words.zip).

### Build Language Model

The Language model can be built using Moses Toolkit
```
MOSESDIR=/path/to/moses
$MOSESDIR/bin/lmplz -o 3 < books.txt > arpa
$MOSESDIR/bin/build_binary arpa LM.en
rm resources/arpa
```
