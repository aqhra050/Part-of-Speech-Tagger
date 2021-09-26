#This file will be used to "train" the HMM model, by creating tables that shall be used to evaluate likelihood and prior probabilities
#We begin by opening the appropiate file

import re

def probabilityGenerate(absoluteTable):
    probabilityTable = {}
    for outerPOS, outerPOS_Dict in absoluteTable.items():
        #getting the total whereby each element 
        outerPOS_total = sum(outerPOS_Dict.values())
        probabilityTable[outerPOS] = {k:v/outerPOS_total for (k, v) in outerPOS_Dict.items()}
    return probabilityTable

def main():
    TRAINING_FILE = "WSJ_24.pos"
    #dictionary will contain a dictionary entry for POS and said entry will contain details key-value pairs of each word having that POS and its count
    absoluteLikelihood = {}
    #dictionary will contain a dictionary entry for POS X and said entry will contain details key-value pairs of each POS Y that is subsequent to POS Y and the count of Y will be noted
    absoluteTransition = {}
    with open(TRAINING_FILE, "r") as trainingFile:
        #will be used to track the ending of sentences (and implicitly the beginning of sentences)
        sentenceEnd   = False
        previousTag   = "Begin_Sent"
        for line in trainingFile:
            if (re.match(r"^\s+$", line)):
                sentenceEnd = True
                word = "End_sent"
                presentTag = "End_sent"
            else:
                line = line.strip()
                word, presentTag = line.split()
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
    #adding a manual entry for the likelihood of the "Begin_Sent" tag
    likelihood["Begin_Sent"] = {"Begin_Sent": 1}
    transitions = probabilityGenerate(absoluteTransition)

    # #Displaying the absoluteLikelihood
    # for POS, WordDict in absoluteLikelihood.items():
    #     print(POS)
    #     for word, count in WordDict.items():
    #         print(f"\t{word:<15} | {count}")
    #     print()

    #Displaying the absoluteTransition
    # for POS, WordDict in absoluteTransition.items():
    #     print(POS)
    #     for word, count in WordDict.items():
    #         print(f"\t{word:<15} | {count}", end=" + ")
    #     print()

    #Displaying the likelihood
    for POS, WordDict in likelihood.items():
        print(f"{POS}")
        for word, count in WordDict.items():
            print(f"\t{word:<15} | {count:.5f}")
        print()

    # #Displaying the transitions
    # for POS, WordDict in transitions.items():
    #     print(f"{POS}")
    #     for word, count in WordDict.items():
    #         print(f"\t{word:<8} | {count:.5f}")
    #     print()



if __name__ == "__main__":
    main()
