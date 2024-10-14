import json
import os
from Functions import getFirtValueAsNum, normalize


class NLP:
    def __init__(self, fileName: str, text: str, nlp):
        self.fileName = fileName
        self.text = text
        self.nlp = nlp
        self.doc = None
        self.tokens = None
        self.entityCount = None
        self.tokenCount = None
        self.entities = None

    def __str__(self):
        return self.fileName + " processor"

    def procesData(self):
        print("process", self.fileName)
        self.doc = self.nlp(self.text)
        # sets normalized all tokens that are not stop words or any punctuation
        self.tokens = [normalize(token.lemma_) for token in self.doc if
                       not token.is_punct and not token.is_stop and not token.is_space]
        self.tokenCount = len(self.tokens)
        self.entities = [normalize(ent.lemma_) for ent in self.doc.ents]
        self.entityCount = len(self.entities)

    def getEntities(self) -> list:
        return self.entities

    def getTokens(self) -> list:
        return self.tokens

    def getTokenCount(self) -> int:
        return self.tokenCount

    def getEntityCount(self) -> int:
        return self.entityCount

    def getFileName(self) -> str:
        return self.fileName

    def getTokenDict(self) -> dict:
        tokensDict = {}
        for token in self.tokens:
            tokensDict[token] = tokensDict.get(token, 0) + 1
        tokensDict["_count"] = self.tokenCount
        return tokensDict

    def getEntityDict(self) -> dict:
        entityDict = {}
        for ent in self.entities:
            entityDict[ent] = entityDict.get(ent, 0) + 1
        entityDict["_count"] = self.entityCount
        return entityDict

    def writeToJSON(self, filePath: str):
        with open(filePath + self.fileName + ".json", "w", encoding="utf-8") as file:
            json.dump({"tokens": self.getTokenDict(), "entities": self.getEntityDict()}, file,
                      ensure_ascii=False, indent=4)


class Ranker:
    def __init__(self, path: str):
        self.path = path
        files = [f for f in os.listdir(path) if os.path.isfile(path + "/" + f)]
        data = {}
        for file in files:
            with open(path + "/" + file, "r", encoding="utf-8") as content:
                data[file] = json.load(content)
                # print(type(data[file]))
        self.JSON_files = data

    def getData(self):
        return self.JSON_files

    def lookup(self, search_doc):
        results = []
        lemmas = [normalize(token.lemma_) for token in search_doc if not token.is_space and not token.is_punct]
        for file in self.JSON_files:  # loops through the json files
            point = 0
            notnullPointCount = 0
            points = []
            tokenDic = self.JSON_files[file]["tokens"]

            for lemma in lemmas:
                buffer = tokenDic.get(lemma, 0)  # gets the lemma from the files tokens json
                points.append(buffer)
                if buffer > 0:
                    notnullPointCount += 1
                # point += buffer if buffer > 0 else 0 - ((tokenDic["_count"] / (len(tokenDic) - 1)) * 2) #this is an old method of point counting
            # new method for
            if notnullPointCount > 0:
                for i in points:
                    if i > 0:
                        point += i
                    else:
                        point -= (tokenDic["_count"] / (len(tokenDic) - 1)) * (sum(points) / notnullPointCount)
            else:
                point = -1  # the value doesn't matter until: 0 >= value

            if point > 0:
                results.append({file[:-5]: point / (tokenDic["_count"] - 1)})  # adds to the list the weighted points

        results.sort(key=getFirtValueAsNum, reverse=True)
        results = [list(item.keys())[0] for item in results]
        return results
