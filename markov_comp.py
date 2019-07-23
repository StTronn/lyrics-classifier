import math
import sys

class MarkovModel():
    def __init__(self,k,s):
        self.counts={}
        self.s=s
        self.k=k
        self.alpha_count=self.count_alphabet()
        self.count_p()
    
    def count_p(self):
        for i in range(len(self.s)-self.k+1):
            ##p
            if self.s[i:i+self.k] in self.counts:
                self.counts[self.s[i:i+self.k]]+=1
            else:
                self.counts[self.s[i:i+self.k]]=1
            ##p.c                   
            if self.s[i:i+self.k+1] in self.counts:
                self.counts[self.s[i:i+self.k+1]]+=1
            else:
                self.counts[self.s[i:i+self.k+1]]=1
       
        ##treating string as circular
        for i in range(1,self.k):
            start=len(self.s)-i
            string = self.s[start:]+self.s[:self.k-i]
            if string in self.counts:
                self.counts[string]+=1
            else:
                self.counts[string]=1
            ##p.c    
            string=string + self.s[self.k-i]
            if string in self.counts:
                self.counts[string]+=1
            else:
                self.counts[string]=1

    def count_alphabet(self):
        l=[]
        for i in self.s:
            if i not in l:
                l.append(i)
        return len(l)

    def laplace(self,c):
        if c in self.counts:
            pc_count = self.counts[c]
        else:
            pc_count=0
        p=c[:self.k]
        if p in self.counts:
            p_count= self.counts[p]
        else:
            p_count= 0
        pr_laplace=(pc_count+1)/(p_count+self.alpha_count)
        return math.log(pr_laplace) 


class likelihood():
    """takes a markov model m and a s computes probaility of ngrams in s using m"""

    def __init__(self,m,s):
        self.probs={}
        self.count=0
        self.average=0
        self.total=0
        k= m.k+1
        for i in range(len(s)-k+1):
                string=s[i:i+k]
                self.probs[string]=m.laplace(string)
                self.count+=1
                self.total+=self.probs[string]            
        ##treating string as circular
        for i in range(1,k):
            start=len(s)-i
            string = s[start:]+s[:k-i]
            self.probs[string]=m.laplace(string)
            self.count+=1
            self.total+=self.probs[string]
        self.average = self.total/self.count


if __name__ == "__main__":
    if len(sys.argv)<=3: 
        model1_text =open("taylor_swiftcorpus.txt").read().strip().replace("\n","")
        model2_text = open("ed_sheerancorpus.txt").read().strip().replace("\n","")
        test = open("red.txt").read().strip().replace("\n","")
        name1="ed sheeran"
        name2="taylor swift"
    else:
        model1_text=open(sys.argv[1]).read().strip().replace("\n","")
        model2_text=open(sys.argv[2]).read().strip().replace("\n","")
        test=open(sys.argv[3]).read().strip().replace("\n","")
        name1=sys.argv[1].replace("corpus.txt","")
        name2=sys.argv[2].replace("corpus.txt","")
    
    model1=MarkovModel(2,model1_text)
    model2=  MarkovModel(2,model2_text)

    sample_with_model1=likelihood(model1,test)
    sample_with_model2=likelihood(model2,test)
    
    avergae_diff=sample_with_model1.average-sample_with_model2.average
    if (avergae_diff>0):
        print(name1,"probability log average diff: ",avergae_diff)
    else:
        print(name2,"probability log average diff: ",avergae_diff)

