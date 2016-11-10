import sys
import getopt
import os
import math
import  re
import operator

class Sentiment_Analyzer :
    class TrainSplit:
        def __init__(self):
            self.train =[]
            self.test =[]

    class Example:
        def __init__(self):
            self.klass = ''
            self.words =[]
    # Sentiment_Analyzer initialization
    def __init__(self):
        self.stopList = set(self.readFile('../data/english.stop'))
        self.numFolds =10
        pass
    def classify(self,words):
        pass
    
    def addExample(self,klass,words):
        text = " ".join(words)
        print text
        hits_excellent =
        hits_excellent =0.01
        hits_poor =0.01
        hits_phrase_near_excellent =0.01
        hits_phrase_near_poor =0.01
        resultexcellent = re.findall(r'execellent',text)
        resultpoor = re.findall(r'poor',text)
        hits_excellent += len(resultexcellent)
        hits_poor += len(resultpoor)
        first_regular_expression = r'[a-zA-Z]+_JJ_(I|B|O)-?([A-Z]+)?\s[a-zA-z]+_(NN|NNS)_(I|B|O)-([A-Z]+)?'
        
        print len(re.findall(first_regular_expression,text))
        second_regular_expession = r'[a-zA-Z]+_(RBR|RB|RBS)_(I|B|O)-?([A-Z]+)?\s[a-zA-z]+_(JJ)_(I|B|O)-([A-Z]+)?'
        second_regular_expression_exclude_this = r'[a-zA-Z]+_(RBR|RB|RBS)_(I|B|O)-?([A-Z]+)?\s[a-zA-z]+_(JJ)_(I|B|O)-([A-Z]+)?\s[a-zA-Z]+_(NN|NNS)_(I|B|O)-?([A-Z]+)?'
        length_second = len(re.findall(second_regular_expession,text))
        length_second -= len(re.findall(second_regular_expression_exclude_this,text))
        print length_second
        third_regular_expression = r'[a-zA-Z]+_(JJ)_(I|B|O)-?([A-Z]+)?\s[a-zA-z]+_(JJ)_(I|B|O)-([A-Z]+)?'
        third_regular_expression_exclude_this = r'[a-zA-Z]+_(JJ)_(I|B|O)-?([A-Z]+)?\s[a-zA-z]+_(JJ)_(I|B|O)-([A-Z]+)?\s[a-zA-Z]+_(NN|NNS)_(I|B|O)-?([A-Z]+)?'
        length_third = len(re.findall(third_regular_expression,text)) -len(re.findall(third_regular_expression_exclude_this,text))
        print length_third
        fourth_regular_expression = r'[a-zA-Z]+_(NN|NNS)_(I|B|O)-?([A-Z]+)?\s[a-zA-z]+_(JJ)_(I|B|O)-([A-Z]+)?'
        fourth_regular_expression_exclude_this = r'[a-zA-Z]+_(NN|NNS)_(I|B|O)-?([A-Z]+)?\s[a-zA-z]+_(JJ)_(I|B|O)-([A-Z]+)?\s[a-zA-Z]+_(NN|NNS)_(I|B|O)-?([A-Z]+)?'
        length_fourth = len(re.findall(fourth_regular_expression,text)) -len(re.findall(fourth_regular_expression_exclude_this,text))
        print length_fourth
        fifth_regular_expression = r'[a-zA-Z]+_(RBR|RBS|RB)_(I|B|O)-?([A-Z]+)?\s[a-zA-z]+_(VB|VBD|VBN|VBG)_(I|B|O)-([A-Z]+)?'
        length_fifth =len(re.findall(fifth_regular_expression,text))
        print length_fifth

    def readFile(self,fileName):
        contents  =[]
        f = open(fileName)
        for line in f:
            contents.append(line)
        f.close()
        result = self.segmentWords('\n'.join(contents))
        return result

    def segmentWords(self,s):
        return s.split()

    def trainSplit(self,trainDir):
        split = self.TrainSplit()
        posTrainFileNames = os.listdir('%s/pos/'%trainDir)
        negTrainFileNames = os.listdir('%s/neg/'%trainDir)
        for fileName in posTrainFileNames:
            example = self.Example()
            example.words = self.readFile('%s/pos/%s'%(trainDir,fileName))
            example.klass = 'pos'
            split.train.append(example)
        for fileName in negTrainFileNames:
            example = self.Example()
            example.words = self.readFile('%s/neg/%s'%(trainDir,fileName))
            example.klass = 'neg'
            split.train.append(example)
        return split


    def crossValidationSplits(self):
        splits  =[]
        i=0
        trainDir = "../data/output_pos"
        posTrainFileNames = os.listdir('%s/positive_pos/'%trainDir)
        #print posTrainFileNames[:5]
        negTrainFileNames = os.listdir('%s/negative_pos/'%trainDir)
        for fold in range(0,1):
            split = self.TrainSplit()
            
            
            for fileName in posTrainFileNames:
                i+=1
                #print fileName,i
                example = self.Example()
                example.words = self.readFile('%s/positive_pos/%s' % (trainDir, fileName))
                example.klass = 'pos'
                if fileName[2] == str(fold):
                    split.test.append(example)
                else:
                    split.train.append(example)
                   
            '''
            for fileName in negTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/negative_pos/%s' % (trainDir, fileName))
                example.klass = 'neg'
                if fileName[2] == str(fold):
                    split.test.append(example)
                else:
                    split.train.append(example)
                    
            '''
            splits.append(split)
        return splits


def test10Fold():
    sent_analyz = Sentiment_Analyzer()
    splits = sent_analyz.crossValidationSplits()
    avgAccuracy = 0.0
    fold =0
    for split in splits[:1]:
        classifier = Sentiment_Analyzer()
        accuracy = 0.0
    
        for example in split.train[:1]:
            words = example.words
            #classifier.addExample(example.klass,words)
    
        for example in split.test[:1]:
            
            words = example.words
            classifier.addExample(example.klass,example.words)
            guess = classifier.classify(words)
            if example.klass == guess:
                accuracy +=1.0
                
        
        accuracy = accuracy / len(split.test)
        avgAccuracy +=accuracy
        print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy)
        fold+=1
    #avgAccuracy = avgAccuracy / fold
    print '[INFO]\tAccuracy: %f' % avgAccuracy


def main():
    sent_analyz = Sentiment_Analyzer()
    test10Fold()


if __name__ == "__main__":
    main()
