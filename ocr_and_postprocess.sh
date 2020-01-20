



INPUT_PDF=$1
OUTPUT=$2
INITPAGE=$3
FINPAGE=$4



SCRIPTDIR=$(dirname $(readlink -f "$0")) #path of ththis script

OUTPUTRAW=$OUTPUT".raw"
REPL_DICT='replacement_dictionary'



#DO OCR
bash $SCRIPTDIR/ocr/do_OCR.sh $INPUT_PDF $OUTPUTRAW $INITPAGE $FINPAGE



#POSTPROCESS
python $SCRIPTDIR/postprocess/get_replacement_dict.py $OUTPUTRAW > $REPL_DICT
python $SCRIPTDIR/postprocess/postprocess_text.py $OUTPUTRAW $REPL_DICT > $OUTPUT

