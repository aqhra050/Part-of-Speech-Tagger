#This file will be used to "train" the HMM model, by creating tables that shall be used to evaluate likelihood and prior probabilities
#We begin by opening the appropiate file
import re, math

def probabilityGenerate(absoluteTable):
    probabilityTable = {}
    for outerPOS, outerPOS_Dict in absoluteTable.items():
        #getting the total whereby each element 
        outerPOS_total = sum(outerPOS_Dict.values())
        probabilityTable[outerPOS] = {k: math.log(v/outerPOS_total) for (k, v) in outerPOS_Dict.items()}
    return probabilityTable

def main(TRAINING_FILE):
    #dictionary will contain a dictionary entry for POS and said entry will contain details key-value pairs of each word having that POS and its count
    absoluteLikelihood = {}
    #dictionary will contain a dictionary entry for POS X and said entry will contain details key-value pairs of each POS Y that is subsequent to POS Y and the count of Y will be noted
    absoluteTransition = {}
    #dictionary will contain all the unique words found
    wordDict = {}

    with open(TRAINING_FILE, "r") as trainingFile:
        #will be used to track the ending of sentences (and implicitly the beginning of sentences)
        sentenceEnd   = False
        previousTag   = "Begin_Sent"
        for line in trainingFile:
            if (re.match(r"^\s+$", line)):
                sentenceEnd = True
                word = "End_Sent"
                presentTag = "End_Sent"
            else:
                line = line.strip()
                word, presentTag = line.split()
                wordDict[word] = True
            #creating an entry into absoluteLikeLihood, as in likelihood entry denominated in frequency
            #will check if a previous entry exists for the given presentTag, if not one is created, an entry for End_Sent will also be created as it stands
            if presentTag not in absoluteLikelihood:
                absoluteLikelihood[presentTag] = {}
            absoluteLikelihood[presentTag][word] = absoluteLikelihood[presentTag].get(word, 0) + 1
            #creating an entry into absoluteTransition
            if previousTag not in absoluteTransition:
                absoluteTransition[previousTag] = {}
            absoluteTransition[previousTag][presentTag] = absoluteTransition[previousTag].get(presentTag, 0) + 1
            #updating the previousTag to be the presentTag in prepartion for the next iteration
            #the start of the new sentence should have as previous the "Begin_Sent" POS
            if sentenceEnd:
                previousTag = "Begin_Sent"
                sentenceEnd = False
            else:
                previousTag = presentTag
    
    #Having generated frequency tables, we now need to generate probability tables

    likelihood = probabilityGenerate(absoluteLikelihood)
    #adding a manual entry for the likelihood of the "Begin_Sent" tag, since I have shifted to log it is set to 0
    likelihood["Begin_Sent"] = {"Begin_Sent": 0}
    transitions = probabilityGenerate(absoluteTransition)
    transitions["End_Sent"] = {}

    return likelihood, transitions, wordDict



if __name__ == "__main__":
    print("NOT TO BE INVOKED DIRECTLY, INVOKE ajc957_main.py")
