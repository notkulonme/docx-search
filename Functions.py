from docx import Document
from unidecode import unidecode


def isLatinNumeral(string: str) -> bool:
    latinNums = ['I', 'V', 'X', 'L', 'C', 'D', 'M', '.']
    for letter in string:
        if not letter in latinNums:
            return False
    return True


def lower_uppered(string: str) -> str:
    arr = string.split(' ')
    for i in range(len(arr)):
        if arr[i].isupper() and not isLatinNumeral(arr[i]):
            arr[i] = arr[i].lower()
    return ' '.join(arr)


def getProcessedText(file: str) -> str:
    docx = Document(file)
    fullText = []
    for paragraph in docx.paragraphs:
        fullText.append(lower_uppered(paragraph.text.strip()))
    return ' '.join(fullText)


def getFirtValueAsNum(dic):
    return float(list(dic.values())[0])


def normalize(token: str):
    return unidecode(token.lower())

