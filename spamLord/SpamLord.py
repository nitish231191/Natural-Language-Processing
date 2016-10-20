import sys
import os
import re
import pprint


my_first_pat = '(\w+)@(\w+).edu' or '\w+\s*@\s*\w+\.?edu'
my_second_pat ='[a-zA-Z0-9|-]+\s*@\s*[a-zA-Z0-9|-]+\s*\.?\s*[a-zA-z0-9|-]+\s*\.\s*[a-zA-z0-9|-]+'
my_third_pat = "obfuscate\s*[(][']\s*[a-zA-Z0-9]+\.?\s*[a-zA-Z0-9]+\s*\.\s*[a-zA-Z0-9]+\s*[']\s*[,]\s*[']\s*[a-zA-Z0-9]+\s*[']\s*[)]"
my_phone_pat='\(?\+?1?\)?\(?\s*[0-9][0-9][0-9]\s*\)?\s*-?\s*[0-9]\s*[0-9]\s*[0-9]-[0-9]\s*[0-9]\s*[0-9]\s*[0-9]\s*'
my_fifth_pat ='[a-zA-Z0-9|-]+\s*[a-zA-Z0-9|-]?at\s*[a-zA-Z0-9|-]+\s*dot?(?!;)\s*[a-zA-Z0-9|-]+\s*dot(?!;)\s*[a-zA-Z0-9]+'
my_phone_pat2 ='\(?\+1\)?\s*[0-9|\s*]{3}\s*[0-9|\s*]{3}\s*[0-9|\s*]{4}'
my_hash_pat ='\w+[&|#|\*]+\w+;\w+\.?\w+\.\w+'
"""
TODO
This function takes in a filename along with the file object (actually
a StringIO object) and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

NOTE: ***don't change this interface***

NOTE: You shouldn't need to worry about this, but just so you know, the
'f' parameter below will be of type StringIO. So, make
sure you check the StringIO interface if you do anything really tricky,
though StringIO should support most everything.
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    for line in f:
        line = line.lower()
        matches = re.findall(my_second_pat,line,re.VERBOSE | re.I)
        phonematch = re.findall(my_phone_pat,line)
        obsfucationmatch = re.findall(my_third_pat,line)
        dotmatch = re.findall(my_fifth_pat,line)
        spacephonematch = re.findall(my_phone_pat2,line)
        hashmatch = re.findall(my_hash_pat,line)
        for  m in hashmatch:
            m = str(m)
            indexsp= m.index('&')
            indexing = m.index(';')
            m = m[:indexsp]+m[indexing:]
            m = re.sub(' *','',m)
            m = re.sub('-','',m)
            m = m.replace(';','@')
            if (name,'e',m) not in res:
                res.append((name,'e',m))


        for m in matches:
            test = m.split('@ or AT or At or at')
            if test:
                email = '%s' % m
                email =re.sub(' *','',email)
                email = re.sub('-','',email)
                tuple2 = (name,'e',email)
                if not tuple2 in res:
                    res.append((name,'e',email))

        for m in phonematch:

            #print "first phone mathes",m
            phone = '%s' % m
            phone = re.sub(' *','',phone)
            phone =re.sub('[()]', '', phone)
            phone = re.sub('-','',phone)
            phone = phone[:3]+'-'+phone[3:6]+'-'+phone[6:]
            phone = phone.strip('\n')
            phone = phone.strip('\t')
            phone = phone.replace('\n','')
            phone = phone.replace('\t','')
            tuple1 = (name,'p',phone)
            if not tuple1 in res:
                #print "Tuple to be added",tuple1
                res.append((name,'p',phone))
        for m in spacephonematch:
            phonespace = '%s'% m
            phonespace = re.sub(' *','',phonespace)
            phonespace = phonespace.replace('+1','')
            phonespace = phonespace[0:3]+'-'+phonespace[3:6]+'-'+phonespace[6:]
            if (name,'p',phonespace) not in res:
                res.append((name,'p',phonespace))
        for m in obsfucationmatch:
            #print "obsfucatio nmatches",m,name
            m = str(m)
            m=m.replace('obfuscate','')
            m= re.sub(' *','',m)
            m = re.sub('[()]','',m)
            m= re.sub('-','',m)
            m=re.sub("\'",'',m)
            m= re.sub(',','@',m)
            index = m.index('@')
            if index ==0 or index == len(m)-1:
                m = m[1:]
                index = m.index('@')
            else:
                email =m[index+1:len(m)]+'@'+m[:index]
            #print "Final" ,email
            tupleobs=(name,'e',email)
            if not tupleobs in res:
                res.append(tupleobs)
        for m in dotmatch:
            #print "dot matches",m
            m = str(m)
            m = re.sub(' *','',m)
            m = re.sub('[()]','',m)
            m= re.sub('-','',m)
            m = re.sub("\'",'',m)
            m = re.sub(',','@',m)
            m = m.replace('at','@')
            m = m.replace('dot','.')
            tupledot =(name,'e',m)
            if not tupledot in res:
                res.append(tupledot)
            #es.append((name,'e',email))
    return res

"""
You should not need to edit this function, nor should you alter
its interface
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    files =[]
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        f = open(path,'r')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not need to edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not need to edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    print 'Guesses (%d): ' % len(guess_set)
    pp.pprint(guess_set)
    print 'Gold (%d): ' % len(gold_set)
    pp.pprint(gold_set)
    print 'True Positives (%d): ' % len(tp)
    pp.pprint(tp)
    print 'False Positives (%d): ' % len(fp)
    pp.pprint(fp)
    print 'False Negatives (%d): ' % len(fn)
    pp.pprint(fn)
    print 'Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn))

"""
You should not need to edit this function.
It takes in the string path to the data directory and the
gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print 'usage:\tSpamLord.py <data_dir> <gold_file>'
        sys.exit(0)
    main(sys.argv[1],sys.argv[2])
