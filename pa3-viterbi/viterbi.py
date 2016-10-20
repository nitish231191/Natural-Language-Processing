import sys
import os
import math
import sys
class Viterbi:
    def __init__(self):
        pass

    def splitlines(self,line):
        wordlist =[]
        templist = line.split("\n")
        line = str(templist[0])
        wordlist = line.split(" ")
        return wordlist

    def predictsequence(self,words, prob_diction,tags):
        resultlist =['phi' for x in range(0, len(words))]
        transition_prob =0.0001
        emission_prob =0.0001
        viterbi_path = [[0 for x in range(0, len(words))] for x in range(0 , len(tags))]
        back_pointer = [[0 for x in range(0, len(words))] for x in range(0 , len(tags))]
        forward_path = [[0 for x in range(0, len(words))] for x in range(0 , len(tags))]
        current_tags= tags[1:len(tags)-1]
        maximum_value = -(sys.float_info.max)
        holding_maximum = maximum_value
        max_pointer =0
        start_tags = tags[0]
        end_tag =tags[len(tags)-1]

        for  i in range(0 ,len(current_tags)):
            transition_prob =0.0001
            emission_prob =0.0001
            if (current_tags[i] ,start_tags) in prob_diction:
                transition_prob = prob_diction[(current_tags[i],start_tags)]
            if (words[0], current_tags[i]) in prob_diction:
                emission_prob = prob_diction[(words[0],current_tags[i])]
            viterbi_path[i][0] = math.log10(transition_prob)+math.log10(emission_prob)
            forward_path[i][0] = transition_prob*emission_prob
            back_pointer[i][0] = 0

        for k in range(1, len(words)):
            for  i in range(0,len(current_tags)):
                emission_prob =0.0001
                if (words[k], current_tags[i]) in prob_diction:
                    emission_prob = prob_diction[(words[k],current_tags[i])]
                maximum_value =holding_maximum
                for j in range(0, len(current_tags)):
                    transition_prob =0.0001
                    if (current_tags[i] ,current_tags[j]) in prob_diction:
                        transition_prob = prob_diction[(current_tags[i],current_tags[j])]

                    current_value = math.log10(transition_prob)+viterbi_path[j][k-1]
                    current_value_forward = transition_prob*forward_path[j][k-1]
                    forward_path[i][k]= forward_path[i][k]+current_value_forward
                    if current_value > maximum_value:
                        maximum_value = current_value
                        max_pointer = j
                viterbi_path[i][k] = maximum_value +math.log10(emission_prob)
                forward_path[i][k] = forward_path[i][k] *emission_prob
                back_pointer[i][k] = max_pointer

        maximum_value =holding_maximum
        max_pointer = 0
        for  i in range(0 ,len(current_tags)):
            transition_prob =0.0001
            if (end_tag, current_tags[i]) in prob_diction:
                transition_prob = prob_diction[(end_tag,current_tags[i])]

            current_value = viterbi_path[i][len(words)-1] +math.log10(transition_prob)

            current_value_forward = forward_path[i][len(words)-1]*transition_prob
            forward_path[len(current_tags)][len(words)-1] += current_value_forward

            if current_value > maximum_value:
                maximum_value = current_value
                max_pointer =i

        viterbi_path[len(current_tags)][len(words)-1] = maximum_value
        back_pointer[len(current_tags)][len(words)-1] = max_pointer

        resultlist[len(words)-1] = current_tags[max_pointer]

        wordindex = len(words)-1
        i = len(current_tags)

        counter =len(words)-2

        for j in range(len(words)-2,-1,-1):
            maxvalue =holding_maximum
            maxpointer =-1
            for i in range(0,len(current_tags)):

                if maxvalue < (viterbi_path[i][j]):
                    maxvalue = (viterbi_path[i][j])
                    maxpointer=i;

            resultlist[counter] = current_tags[maxpointer]
            counter= counter-1

        print "PROCESSING SENTENCE :",
        for i in range(0,len(words)):
            print words[i],

        print "\n"
        print "FINAL VITERBI NETWORK"
        for i in range(0,len(words)):
            for j in range(0,len(current_tags)):
                print "P("+words[i]+"="+current_tags[j]+")"+" = "+ str(pow(10,viterbi_path[j][i]))

        print "\n"
        print "FINAL BACKPOINTER NETWORK"
        for i in range(len(words)-1,0,-1):
            for j in range(0,len(current_tags)):
                print "Backptr("+words[i]+"="+current_tags[j]+")"+"="+ current_tags[back_pointer[j][i]]

        print "\n"
        print "BEST TAG SEQUENCE HAS PROBABILITY =",pow(10,viterbi_path[len(current_tags)][len(words)-1])
        for i in range(len(words)-1,-1,-1):
            print words[i],"->",resultlist[i]

        print "\n"
        print "FORWARD ALGORITHM RESULTS"

        for i in range(0 , len(words)):
            for j in range(0,len(current_tags)):
                print "P("+words[i]+"="+current_tags[j]+")"+" = "+ str(forward_path[j][i])

        print "\n"
        return resultlist

    def identifiytagsfromprobabiltyfile(self,line):
        pass

def main():
    if(len(sys.argv)!=3):
        print "Please provide two arguments"
        sys.exit(0)
    wordlist =[]
    problist =[]
    probs = sys.argv[1]
    sentences = sys.argv[2]
    probs_file_id = open(probs,"r")
    sent_file_id = open(sentences,"r")
    vb =Viterbi()
    for line in sent_file_id:
        wordlist.append(vb.splitlines(line))
    tags = ["phi","noun","verb","inf","prep","fin"]
    probab_dict = {}
    for line in probs_file_id:
        problist.append(vb.splitlines(line))
    for prob in problist:
        probab_dict[(prob[0],prob[1])]=float(prob[2])
    for i in range(0,len(wordlist)):
        vb.predictsequence(wordlist[i],probab_dict,tags)



if __name__ == '__main__':
    main()
