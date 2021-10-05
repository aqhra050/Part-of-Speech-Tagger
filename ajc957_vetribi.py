from numpy.core.fromnumeric import transpose
import ajc957_trainHMM
import numpy as np
import re, math

def extractSentences(DEVELOPMENT_FILE):
    #this will generate individual where each sentence is demarcated by a blank link
    sentences = []

    with open(DEVELOPMENT_FILE, "r") as developmentFile:
        #will be used to store sentences as formulated as a stream of tokens
        #will be used to store the tokes assossciated with an individual sentence
        tokens = []
        for line in developmentFile:
            #a blank line demarcates the end of a sentence
            if (re.match(r"^\s+$", line)):
                sentences.append(tokens)
                tokens = []
            else:
                word = line.strip()
                tokens.append(word)

    return sentences        

def vetribiAlgorithm(tokens, numPOS, likelihood, transitions, wordList):
    OOV_PROBABILITY = math.log(1/1000)
    tokens = ["Begin_Sent"] + tokens + ["End_Sent"]
    numTokens = len(tokens)
    vetribi = {k: numTokens * [np.NINF] for k in likelihood.keys()}
    contributor = {k:numTokens * [("",-1)] for k in likelihood.keys()}

    np.set_printoptions(linewidth=np.inf)

    #Establishing the First
    vetribi["Begin_Sent"][0] = 0

    for presentTokenPosition in range(1, numTokens):
        presentToken = tokens[presentTokenPosition]
        isOOV = False if presentToken in wordList else True

        previousTokenPosition = presentTokenPosition - 1

        for presentTag in likelihood.keys():
            for possiblePreviousTag in likelihood.keys():
                previousVetribi = vetribi[possiblePreviousTag][previousTokenPosition]
                transitionProbability = transitions[possiblePreviousTag].get(presentTag, -1e15)
                emissionProbability = OOV_PROBABILITY if isOOV else likelihood[presentTag].get(presentToken, np.NINF)
                presentProbability = previousVetribi + transitionProbability + emissionProbability

                if presentProbability > vetribi[presentTag][presentTokenPosition]:
                    vetribi[presentTag][presentTokenPosition] = presentProbability
                    contributor[presentTag][presentTokenPosition] = (possiblePreviousTag, previousTokenPosition)

    reverseTraversal = []
    maxTag, maxPos = contributor["End_Sent"][numTokens - 1]
    while (maxTag != "Begin_Sent"):
        reverseTraversal.append(maxTag)
        maxTag, maxPos = contributor[maxTag][maxPos]

    reverseTraversal.reverse()

    return reverseTraversal
   
def main(TRAINING_FILE, DEVELOPMENT_FILE, OUTPUT_FILE):
    print("TRAINING BEGIN.")
    likelihood, transitions, wordDict = ajc957_trainHMM.main(TRAINING_FILE)
    print("TRAINING END.")
    sentences = extractSentences(DEVELOPMENT_FILE)

    countPOS = len(likelihood.keys())
    # countPOS = len(transitions.keys()) #this will be one lesser than distinctPOS_likelihood since there are no transitions away from the "End_Sent" POS-tag by definition, yet it will have a likelihood of one, hence the above is used instead of this

    # set_distinctPOS_likelihood = set(likelihood)
    # set_distinctPOS_transitions = set(transitions)

    # print(set_distinctPOS_likelihood.difference(set_distinctPOS_transitions))

    count = 0
    with open(OUTPUT_FILE, "w") as outputFile:
        for tokens in sentences:
            tags = vetribiAlgorithm(tokens, countPOS, likelihood, transitions, wordDict)
            tokenAndTags = list(map(lambda x: "\t".join(x), zip(tokens, tags)))
            for tokenAndTag in tokenAndTags:
                outputFile.write(tokenAndTag + "\n")
            outputFile.write("\n")
            print(f"Sentence #{count} done.")
            count += 1

if __name__ == "__main__":
    print("NOT TO BE INVOKED DIRECTLY, INVOKE ajc957_main.py")