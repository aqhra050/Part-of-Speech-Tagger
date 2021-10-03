from numpy.core.fromnumeric import transpose
import trainHMM
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

                # if presentTokenPosition == 7:
                #     print(f"presentProbability is {presentProbability}")
                #     # if transitionProbability > np.NINF:
                #     print(f"({possiblePreviousTag}->{presentTag}) = {transitionProbability}")
                #     # if emissionProbability > np.NINF:
                #     print(f"{presentToken} AS {presentTag} = {emissionProbability}")
                #     # if previousVetribi > np.NINF:
                #     print(f"vetribi({possiblePreviousTag}, {previousTokenPosition}) = {previousVetribi}")
                #     print("-"*80)

                if presentProbability > vetribi[presentTag][presentTokenPosition]:
                    vetribi[presentTag][presentTokenPosition] = presentProbability
                    contributor[presentTag][presentTokenPosition] = (possiblePreviousTag, previousTokenPosition)
        
    # for POS_TAG in vetribi:
    #     print(f"{POS_TAG[:min(len(POS_TAG), 4)]:<4}", end="|")
    #     print(vetribi[POS_TAG])

    # for POS_TAG in contributor:
    #     print(f"{POS_TAG[:min(len(POS_TAG), 4)]:<4}", end="|")
    #     print(contributor[POS_TAG])

    reverseTraversal = []
    maxTag, maxPos = contributor["End_Sent"][numTokens - 1]
    while (maxTag != "Begin_Sent"):
        reverseTraversal.append(maxTag)
        maxTag, maxPos = contributor[maxTag][maxPos]

    reverseTraversal.reverse()

    return reverseTraversal
    # print(tokens)
    # # print(type(tokens))
    # tokens = ["Begin_Sent"] + tokens + ["End_Sent"]
    # numTokens = len(tokens)
    # print(tokens)
    # print(f"Length:{numTokens}")
    # A = {}
    # B = {}
    # for POS_TAG in likelihood.keys():
    #     A[POS_TAG] = np.full(numTokens, np.NINF)
    #     B[POS_TAG] = [("", 0)] * numTokens
    #     # print(POS_TAG, end=" | ")
    # # print(f"\n{'-' * 80}")
    # tokenPosition = 0
    # A["Begin_Sent"][tokenPosition] = 0
    # for tokenPosition in range(1, numTokens):
    #     isOOV = False
    #     presentToken = tokens[tokenPosition]

    #     if tokenPosition == 7:
    #         for POS_TAG in likelihood:
    #             if presentToken in likelihood[POS_TAG]:
    #                 print(f"{presentToken} in {POS_TAG}")

    #     # print(f"Present Token = {presentToken}")
    #     if presentToken not in wordList and presentToken != "End_Sent":
    #         print(f"{presentToken} is an OOV item | wordList")
    #         isOOV = True

    #     maximal = np.NINF
    #     maximalTuple = ("", 0)
    #     contributors = []
    #     for presentTag in likelihood.keys():
    #         maxProbability = np.NINF
    #         maxContributor = ("", 0)
    #         for previousTag in likelihood.keys():
    #             presentProbability = A[previousTag][tokenPosition - 1] + transitions.get(previousTag, {}).get(presentTag, np.NINF) + (OOV_PROBABILITY if isOOV else likelihood[presentTag].get(presentToken, np.NINF))
    #             #have had to rely on log addition instead of multiplication because was getting too small a values otherwise

    #             # if tokenPosition == 7:
    #             #     with open("debug.txt", "a") as debugFile:
    #             #         debugFile.write(presentToken + " " + str(tokenPosition) + "\n")
    #             #         debugFile.write(f"{previousTag}|{presentTag}\n")
    #             #         debugFile.write(f"presentProbability is {presentProbability}\n")
    #             #         if A[previousTag][tokenPosition - 1] == 0:
    #             #             debugFile.write(f"A[{previousTag}][{tokenPosition - 1}] is 0\n")
    #             #         if transitions.get(previousTag, {}).get(presentTag, 0) == 0:
    #             #             debugFile.write(f"Transition ({previousTag},{presentTag}) is 0\n")
    #             #         if OOV_PROBABILITY if isOOV else likelihood[presentTag].get(presentToken, 0) == 0:
    #             #             debugFile.write(f"likelihood[{presentTag}][{presentToken}] is 0\n")
    #             #         debugFile.write(f"{A[previousTag][tokenPosition - 1]} {transitions.get(previousTag, {}).get(presentTag, np.NINF)} {OOV_PROBABILITY if isOOV else likelihood[presentTag].get(presentToken, np.NINF)}\n")
    #             #         debugFile.write("-" * 30 + "\n")
    #             # elif tokenPosition > 7:
    #             #     print("STOPPING")


    #             if presentProbability > maxProbability:
    #                 maxProbability = presentProbability
    #                 maxContributor = (previousTag, tokenPosition - 1)
    #                 contributors.append(maxContributor)

    #         A[presentTag][tokenPosition] = maxProbability
    #         B[presentTag][tokenPosition] = maxContributor

    #         if maxProbability > maximal:
    #             maximalTuple = maxContributor
    #     print(f"({maximalTuple[0]}, {maximalTuple[1]}) maximises {presentToken}")
    #     print(contributors)

    # reverseTraversal = []
    # maxTag, maxPos = B["End_Sent"][numTokens - 1]
    # while (maxTag != "Begin_Sent"):
    #     reverseTraversal.append(maxTag)
    #     maxTag, maxPos = B[maxTag][maxPos]

    # reverseTraversal.reverse()
    # return reverseTraversal


if __name__ == "__main__":
    TRAINING_FILE = "increasedTraining.pos"
    DEVELOPMENT_FILE = "WSJ_23.words"
    OUTPUT_FILE = "output.pos"

    print("TRAINING BEGIN.")
    likelihood, transitions, wordDict = trainHMM.main(TRAINING_FILE)
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



    # print(vetribi(["I", "hate", "this"], countPOS, likelihood, transitions))