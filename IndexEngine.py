
import sys
import spacy
from Functions import *
from Classes import *

nlp = spacy.load("hu_core_news_lg")
#nlp.remove_pipe("trainable_lemmatizer")
if len(sys.argv)==2:
    contentDirPath = sys.argv[1]
    print("reading files")
    files = [f for f in os.listdir(contentDirPath) if os.path.isfile(contentDirPath + "/" + f) and f.split(".")[-1] == "docx"]
    print(", ".join(files), "were read", sep="\n")
    os.makedirs(contentDirPath + ".index", exist_ok=True)

    for f in files:
        processor = NLP(f, getProcessedText(contentDirPath + f),nlp)
        processor.procesData()
        processor.writeToJSON(contentDirPath + ".index/")
        del processor



