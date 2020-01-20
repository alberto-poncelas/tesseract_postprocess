#!/bin/bash


INPUT_PDF=$1
OUTPUT=$2
INITPAGE=$3
FINPAGE=$4


# Create and go to a temporal folder where temporal files are produces
SCRIPTDIR=$(dirname $(readlink -f "$0")) #path of ththis script
CURRENTDIR=$(pwd)
TMP_DIR=$(mktemp -d)
cd $TMP_DIR

#cut pdf
pdftk  "$INPUT_PDF" cat "$INITPAGE"-"$FINPAGE" output $TMP_DIR/split.pdf

#convert from pdf to png
pdftoppm -rx 200 -ry 200 -png $TMP_DIR/split.pdf "OCR"


# Do OCR and append to output file
files=$(ls  $TMP_DIR/*.png)
for f in $files; do 
tesseract $f $f"_ocr" -l eng
cat $f"_ocr.txt" >> raw_output
done

python $SCRIPTDIR/fix_linebreaks.py raw_output > output

cd $CURRENTDIR
mv $TMP_DIR/output $OUTPUT
rm -r $TMP_DIR

