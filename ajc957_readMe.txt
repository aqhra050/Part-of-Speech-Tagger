My solution for the Homework Three, employs the following program files: "ajc957_main.py", "ajc957_vetribi.py", and "ajc957_trainHMM.py"
Of these only "ajc957_main.py" may be invoked directly from the terminal and as much invokes "ajc957_vetribi.py" which in turn subsequently invokes "ajc957_trainHMM.py".
The program files "ajc957_vetribi.py" and "ajc957_trainHMM.py" may not be called directly since they require file infromation which is given by "ajc957_main.py".
The invocation of "ajc957_main.py" is as follows:
python3 ajc957_main.py <trainingFile> <inputUntaggedFile> <outputTaggedFile>
Important Notes:
Transition probabilities were considered for bigrams
Out of Vocabulary Items have been handled by assuming a constant small unifrom probability of the given OOV item's emmission across all tages.
Rather than multiplication of small numbers which would sometimes be truncated to zero due to limits of Python's precision, and accordingly log-addition was used in place of multiplication whereby all probabilities are expressed as powers of e.
Additionally, to prevent failure of the algorithm rather than give transitions a log likelihood of -inf for transitions not existing (equivalent to a probability of 0), even transitions that do not exist in the training set are given a log likelihood of greater than -inf (-1e9) that is nonetheless very negative.
An alternate scheme of OOV (treating all unique items as instances of "OOV_ITEM") was tried but this was unsuccessfull, it is available at the link https://github.com/aqhra050/NLP-AssignmentThree, but was not used for submission due to low accuracy.