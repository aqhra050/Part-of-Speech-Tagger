import ajc957_vetribi
import argparse

def main():
    parser = argparse.ArgumentParser(description='Process some files which shall be used for POS tagging.')
    parser.add_argument('trainingFile',  help='This is the file that shall be used for training (should be a .pos)')
    parser.add_argument('inputFile',  help='This is the file that is to be tagged.')
    parser.add_argument('outputFile',  help='This is the file that shall contain tags.')
    args = parser.parse_args()
    ajc957_vetribi.main(args.trainingFile, args.inputFile, args.outputFile)


if __name__ == "__main__":
    main()