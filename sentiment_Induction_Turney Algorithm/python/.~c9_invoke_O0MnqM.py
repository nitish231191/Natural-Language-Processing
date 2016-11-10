import sys
import getopt
import os
import string
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
    def filterStopWords(self, words):
        filtered = []
        for word in words:
            if not word in self.stopList and word.strip() != '':
                filtered.append(word)
        return filtered   
        
    def extractWords(self, words):
        regex = r'[a-z0-9]+'
        stringlist = []
        i=0
        for element in re.findall(regex,words):
            stringlist.append(element)
            i=i+1
            
        return  " ".join(stringlist)
        
    def classify(self,words,totalwords):
        #totalwords = self.filterStopWords(totalwords)
        x = [''.join(char for char in word if char not in string.punctuation) for word in totalwords]
        x = [word for word in x if word]
        fulltext = " ".join(x)
        text = " ".join(words)
        #print text
        hits_phrase =[]
        hits_excellent =0.01
        hits_poor =0.01
        hits_phrase_near_excellent =[0.01 for x in range(0,5)]
        hits_phrase_near_poor =[0.01 for x in range(0,5)]
        result = [0 for x in range(0,5)]
        #hits_excellent += len(re.findall(r'excellent\s+',fulltext))
        #hits_poor += len(re.findall(r'poor\s+',fulltext))
        hits_poor +=len(re.findall(r'excellent',fulltext))
        hits_excellent+= len(re.findall(r'poor',fulltext))
        print hits_excellent,hits_poor
        hits_first =[]
        first_regular_expression = r'([a-zA-Z]+_JJ_(I|B|O)-?([A-Z]+)?\s[a-zA-z]+_(NN|NNS)_(I|B|O)-([A-Z]+)?)'
        for m in re.finditer(first_regular_expression,text):
            hits_first.append((m.start(),m.end()))
        first_phrase =[]
        first_phrase_search = []
        first_list = []
        for i in range(0,len(hits_first)):
            textsearch = text[hits_first[i][0]:hits_first[i][1]]
            first_list.append("".join(textsearch))
            
        for i in range(0,len(first_list)):
            first_phrase.append(self.extractWords(first_list[i]))
            
        hits_first_phrase =[]
        for i in range(0,len(first_phrase)):
            for m in re.finditer(re.compile(first_phrase[i]),fulltext):
                hits_first_phrase.append((m.start(),m.end()))
                
        for j in range(0,len(hits_first_phrase)):
            first_phrase_search.append(self.searchNEAR(hits_first_phrase,j,fulltext))
            
       
            
        #print first_phrase_search
            
        # skipping phrases when both phrase near excellent and phrase near poor are less than or equal to 1
        for i in range(0,len(first_phrase_search)):
            hits_phrase_near_excellent[0] =0.01 
            hits_phrase_near_poor[0] =0.01
            if  (len(re.findall(r'excellent\s+',first_phrase_search[i])) <=1) and (len(re.findall(r'poor\s+',first_phrase_search[i]))<=1):
                hits_phrase_near_excellent[0]=0.01
                hits_phrase_near_poor[0] =0.01
            else:
                hits_phrase_near_excellent[0]+=len(re.findall(r'excellent\s+',first_phrase_search))
                hits_phrase_near_poor[0] += len(re.findall(r'poor\s+',first_phrase_search))
            #print hits_phrase_near_excellent[0],hits_phrase_near_poor[0]
            #print (math.log(hits_phrase_near_excellent[0],2)+math.log(hits_poor,2)) -(math.log(hits_phrase_near_poor[0],2) +math.log(hits_excellent,2))
            result[0]  += (math.log(hits_phrase_near_excellent[0],2)+math.log(hits_poor,2)) -(math.log(hits_phrase_near_poor[0],2) +math.log(hits_excellent,2))
        
        print "result",result[0]
        if len(first_phrase_search)>0:
            result[0] = result[0]/len(first_phrase_search)
        hits_second = []
        second_regular_expession = r'[a-zA-Z]+_(RBR|RB|RBS)_(I|B|O)-?([A-Z]+)?\s[a-zA-z]+_(JJ)_(I|B|O)-([A-Z]+)?'
        for m in re.finditer(second_regular_expession,text):
            hits_second.append((m.start(),m.end()))
        second_regular_expression_exclude_this = r'[a-zA-Z]+_(RBR|RB|RBS)_(I|B|O)-?([A-Z]+)?\s[a-zA-z]+_(JJ)_(I|B|O)-([A-Z]+)?\s[a-zA-Z]+_(NN|NNS)_(I|B|O)-?([A-Z]+)?'
        for m in re.finditer(second_regular_expression_exclude_this,text):
            for k,(start,end) in enumerate(hits_second):
                if start == m.start():
                    del hits_second[k]
                    
                    
        second_list = []
        second_phrase =[]
        second_phrase_search = []
        for i in range(0,len(hits_second)):
            textsearch = text[hits_second[i][0]:hits_second[i][1]]
            second_list.append("".join(textsearch))
            
        for i in range(0,len(second_list)):
            second_phrase.append(self.extractWords(second_list[i]))
            
        hits_second_phrase =[]
        for i in range(0,len(second_phrase)):
            for m in re.finditer(re.compile(second_phrase[i]),fulltext):
                hits_second_phrase.append((m.start(),m.end()))
            

        for j in range(0,len(hits_second_phrase)):
            second_phrase_search.append(self.searchNEAR(hits_second_phrase,j,fulltext))
    
        
        for i in range(0,len(second_phrase_search)):
            hits_phrase_near_poor[1] =0.01 
            hits_phrase_near_excellent[1] =0.01
            # skipping phrases when both phrase near excellent and phrase near poor are less than or equal to 1
            if  (len(re.findall(r'excellent\s+',second_phrase_search[i])) <=1) and (len(re.findall(r'poor\s+',second_phrase_search[i]))<=1):
                hits_phrase_near_excellent[1]=0.01
                hits_phrase_near_poor[1] =0.01
            else:
                hits_phrase_near_excellent[1]+=len(re.findall(r'excellent\s+',second_phrase_search))
                hits_phrase_near_poor[1] += len(re.findall(r'poor\s+',second_phrase_search))
            
            result[1] += (math.log(hits_phrase_near_excellent[1],2)+math.log(hits_poor,2)) -(math.log(hits_phrase_near_poor[1],2) +math.log(hits_excellent,2))
        
        print "result",result[1]
        if len(second_phrase_search)>0:
            result[1] = result[1]/len(second_phrase_search)
        third_regular_expression = r'[a-zA-Z]+_(JJ)_(I|B|O)-?([A-Z]+)?\s[a-zA-z]+_(JJ)_(I|B|O)-([A-Z]+)?'
        third_regular_expression_exclude_this = r'[a-zA-Z]+_(JJ)_(I|B|O)-?([A-Z]+)?\s[a-zA-z]+_(JJ)_(I|B|O)-([A-Z]+)?\s[a-zA-Z]+_(NN|NNS)_(I|B|O)-?([A-Z]+)?'
        hits_third = []
        for m in re.finditer(third_regular_expression,text):
            hits_third.append((m.start(),m.end()))
            
        for m in re.finditer(third_regular_expression_exclude_this,text):
            for k,(start,end) in enumerate(hits_third):
                if start == m.start():
                    del hits_third[k]
                    
        third_list = []
        third_phrase =[]
        third_phrase_search = []
        for i in range(0,len(hits_third)):
            textsearch = text[hits_third[i][0]:hits_third[i][1]]
            third_list.append("".join(textsearch))
            
        for i in range(0,len(third_list)):
            third_phrase.append(self.extractWords(third_list[i]))
            
        hits_third_phrase =[]
        for i in range(0,len(third_phrase)):
            for m in re.finditer(re.compile(third_phrase[i]),fulltext):
                hits_third_phrase.append((m.start(),m.end()))
            

        for j in range(0,len(hits_third_phrase)):
            third_phrase_search.append(self.searchNEAR(hits_third_phrase,j,fulltext))
        
        # skipping phrases when both phrase near excellent and phrase near poor are less than or equal to 1
        for i in range(0,len(third_phrase_search)):
            hits_phrase_near_excellent[2] =0.01 
            hits_phrase_near_poor[2] =0.01
            if  (len(re.findall(r'excellent\s+',third_phrase_search[i])) <=1) and (len(re.findall(r'poor\s+',third_phrase_search[i]))<=1):
                hits_phrase_near_excellent[2]=0.01
                hits_phrase_near_poor[2] =0.01
            else:
                hits_phrase_near_excellent[2]+=len(re.findall(r'excellent\s+',third_phrase_search[i]))
                hits_phrase_near_poor[2] += len(re.findall(r'poor\s+',third_phrase_search[i]))
                print math.log(hits_phrase_near_excellent[2],2),math.log(hits_poor,2),math.log(hits_excellent,2),math.log(hits_phrase_near_poor[2],2)
            result[2]  += (math.log(hits_phrase_near_excellent[2],2)+math.log(hits_poor,2)) -(math.log(hits_phrase_near_poor[2],2) +math.log(hits_excellent,2))
            
        print "result 2",result[2]
        if len(third_phrase_search)>0:
            result[2] = result[2]/len(third_phrase_search)       
        
        fourth_regular_expression = r'[a-zA-Z]+_(NN|NNS)_(I|B|O)-?([A-Z]+)?\s[a-zA-z]+_(JJ)_(I|B|O)-([A-Z]+)?'
        fourth_regular_expression_exclude_this = r'[a-zA-Z]+_(NN|NNS)_(I|B|O)-?([A-Z]+)?\s[a-zA-z]+_(JJ)_(I|B|O)-([A-Z]+)?\s[a-zA-Z]+_(NN|NNS)_(I|B|O)-?([A-Z]+)?'
        hits_fourth = []
        for m in re.finditer(fourth_regular_expression,text):
            hits_fourth.append((m.start(),m.end()))
            
        for m in re.finditer(fourth_regular_expression_exclude_this,text):
            for k,(start,end) in enumerate(hits_fourth):
                if start == m.start():
                    del hits_fourth[k]
            
        fourth_list = []
        fourth_phrase =[]
        fourth_phrase_search = []
        for i in range(0,len(hits_fourth)):
            textsearch = text[hits_fourth[i][0]:hits_fourth[i][1]]
            fourth_list.append("".join(textsearch))
            
        for i in range(0,len(fourth_list)):
            fourth_phrase.append(self.extractWords(fourth_list[i]))
            
        hits_fourth_phrase =[]
        for i in range(0,len(fourth_phrase)):
            for m in re.finditer(re.compile(fourth_phrase[i]),fulltext):
                hits_fourth_phrase.append((m.start(),m.end()))
            

        for j in range(0,len(hits_fourth_phrase)):
            fourth_phrase_search.append(self.searchNEAR(hits_fourth_phrase,j,fulltext))
            
        # skipping phrases when both phrase near excellent and phrase near poor are less than or equal to 1
        for i in range(0,len(fourth_phrase_search)):
            hits_phrase_near_excellent[3] =0.01 
            hits_phrase_near_poor[3] =0.01
            if  (len(re.findall(r'excellent\s+',fourth_phrase_search[i])) <=1) and (len(re.findall(r'poor\s+',fourth_phrase_search[i]))<=1):
                hits_phrase_near_excellent[3]=0.01
                hits_phrase_near_poor[3] =0.01
            else:
                hits_phrase_near_excellent[3]+=len(re.findall(r'excellent\s+',fourth_phrase_search))
                hits_phrase_near_poor[3] += len(re.findall(r'poor\s+',fourth_phrase_search))
            
            result[3]  += (math.log(hits_phrase_near_excellent[3],2)+math.log(hits_poor,2)) -(math.log(hits_phrase_near_poor[3],2) +math.log(hits_excellent,2))
            
        print "result 3",result[3]
        if len(fourth_phrase_search)>0:
            result[3] = result[3]/len(fourth_phrase_search)
        fifth_regular_expression = r'[a-zA-Z]+_(RBR|RBS|RB)_(I|B|O)-?([A-Z]+)?\s[a-zA-z]+_(VB|VBD|VBN|VBG)_(I|B|O)-([A-Z]+)?'
        hits_fifth = []
        for m in re.finditer(fifth_regular_expression,text):
            hits_fifth.append((m.start(),m.end()))
            
        fifth_list = []
        fifth_phrase =[]
        fifth_phrase_search = []
        for i in range(0,len(hits_fifth)):
            textsearch = text[hits_fifth[i][0]:hits_fifth[i][1]]
            fifth_list.append("".join(textsearch))
        for i in range(0,len(fifth_list)):
            fifth_phrase.append(self.extractWords(fifth_list[i]))
        hits_fifth_phrase =[]
        for i in range(0,len(fifth_phrase)):
            for m in re.finditer(re.compile(fifth_phrase[i]),fulltext):
                hits_fifth_phrase.append((m.start(),m.end()))

        for j in range(0,len(hits_fifth_phrase)):
            fifth_phrase_search.append(self.searchNEAR(hits_fifth_phrase,j,fulltext))
        # skipping phrases when both phrase near excellent and phrase near poor are less than or equal to 1
        for i in range(0,len(fifth_phrase_search)):
            hits_phrase_near_excellent[4] =0.01 
            hits_phrase_near_poor[4] =0.01
            if  (len(re.findall(r'excellent\s+',fifth_phrase_search[i])) <=1) and (len(re.findall(r'poor\s+',fifth_phrase_search[i]))<=1):
                hits_phrase_near_excellent[4]=0.01
                hits_phrase_near_poor[4] =0.01
            else:
                hits_phrase_near_excellent[4]+=len(re.findall(r'excellent\s+',fifth_phrase_search))
                hits_phrase_near_poor[4] += len(re.findall(r'poor\s+',fifth_phrase_search))
            
            result[4]  += (math.log(hits_phrase_near_excellent[4],2)+math.log(hits_poor,2)) -(math.log(hits_phrase_near_poor[4],2) +math.log(hits_excellent,2))
        
        print "result4",result[4]
        
        if len(fifth_phrase_search)>0:
            result[4] = result[4]/(len(fifth_phrase_search))
        summ=0
        for i in range(0,5):
            summ += result[i]
            
        avgsum = summ/5
        
        print "this decides result",avgsum
        if avgsum >0:
            return 'pos'
            
        else:
            return 'neg'
    
    def searchNEAR(self,hits,j,text):
        start = hits[j][0]
        lengthofspaces =0
        for i in range(start-2,-1,-1):
            if text[i] == ' ':
                lengthofspaces+=1
            if lengthofspaces >=10:
                break
        before_text= text[i:start]
        #print before_text
        #print "_____________________"
        lengthofspaces =0

        end = hits[j][1]
        for i in range(end+1,len(text)):
            if text[i] == ' ':
                lengthofspaces+=1
            if lengthofspaces >=10:
                break
                
        
        after_text = text[end+1:i]
        #print after_text
        return before_text+after_text
    def addExample(self,klass,words):
        pass
        
    # Near Operator
        
    def mylistdir(self,path):
        result =[]
        f = os.listdir(path)
        for file in f:
            if not file.startswith('.'):
                result.append(file)
                
        return result

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
        trainDir1  = "../data/imdb1"
        posTrainFileNames = self.mylistdir('%s/positive_pos/'%trainDir)
        negTrainFileNames = self.mylistdir('%s/negative_pos/'%trainDir)
        countnfiles =0
        for fold in range(0, self.numFolds):
            split = self.TrainSplit()
            
            
            for fileName in posTrainFileNames:
                example = self.Example()

                if fileName[2] == str(fold):
                    example.words = self.readFile('%s/positive_pos/%s' % (trainDir, fileName))
                    example.klass = 'pos'
                    split.test.append(example)
                else:
                    example.words = self.readFile('%s/pos/%s' % (trainDir1, fileName))
                    example.klass = 'pos'
                    countnfiles+=1
                    split.train.append(example)
                   
            for fileName in negTrainFileNames:
                example = self.Example()

                if fileName[2] == str(fold):
                    example.words = self.readFile('%s/negative_pos/%s' % (trainDir, fileName))
                    example.klass = 'neg'
                    split.test.append(example)
                else:
                    example.words = self.readFile('%s/neg/%s' % (trainDir1, fileName))
                    example.klass = 'neg'
                    countnfiles +=1
                    #print fileName
                    split.train.append(example)
            print countnfiles        
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
        listofwords =[]
        length =0
        lengthpoor =0
        for example in split.train:
            words = example.words
            length +=words.count('poor')
            lengthpoor+=words.count('excellent')
            listofwords.extend(words)
   
            

            
        for example in split.test:
            #print example.klass
            guess = classifier.classify(words,listofwords)
            if example.klass == guess:
                accuracy +=1.0
        
            
        accuracy = accuracy / 10
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
