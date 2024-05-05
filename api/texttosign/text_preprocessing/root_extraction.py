#### problems
# - احزانى is converted worng
# - يكرهون should only be يكرة without adding ون because it's a verb not a noun 
# - solve the problem of grouping

class ArabicRoot:
    ''' ArabicRoot class is responsible to apply transformation on word to remove prefix or suffix 
        or split the word into multiple words ex : طعامك --> طعام + ملكك
    '''
    
    def __init__(self,word_list):
        self.word_list = word_list
        self.plural = ['ات',"ون","ين","ان"]
        self.mine = ['ني',"تي"]
        

        self.pre6 = ['كال',"بال","فال","مال","ولل","است","يست","تست","مست","وال"]
        self.pre5 = ["سن","ست","سى","لي","لن","لت","لل"]
        self.pre4 = ["ت","ي","ب","ل"]



        self.suf5 = ["ون","ات","ان","ين","تن","تم","كن","كم","هن","هم","يا","ني","تي","وا","ما","نا","ية","ها","اء"]
        self.suf4 = ['ت',"ة","ا","ي"]
        
        # list of extra methods (methods retur the word + other words)
        self.extra_methods = [self.extra_plural,self.extra_feminine,self.extra_ownership]
    
    def remove_prefix(self,word):
        ''' remove prefix from words ex : تشرب --> شرب '''
        if(len(word)>=6):
            for pre in self.pre6:
                if word.startswith(pre):
                    return word[3:]
        if(len(word)>=5):
            for pre in self.pre5:
                if word.startswith(pre):
                    return word[2:]
        if(len(word)>=4):
            for pre in self.pre4:
                if word.startswith(pre):
                    return word[1:]
        
        return word
                
    
    def remove_suffix(self,word):        
        ''' remove suffix from words ex : ياكلون --> ياكل  '''
        if(len(word)>=5):                
            for suf in self.suf5:
                if word.endswith(suf):
                    return word[:-2]
        if(len(word)>=4):
            for suf in self.suf4:
                if word.endswith(suf):
                    return word[:-1]
        
        return word
    
    def clean_word(self,word):
        ''' remove both suffix and prefix '''
        return self.remove_suffix(self.remove_prefix(word))
        
    
    
    
    def extra_plural(self,word):
        ''' if the word is plural then convert it to word +  كثير but i need 
            to make some changes in it to handle verbs being plural when word are plural 
            ex : ['مهندس', 'كثير', 'يكره', 'كثير', 'جامعة']
            also need to return word + كثير even if word not in word_list
        '''
        if(len(word)>=5):                
            for suf in self.plural:
                if word.endswith(suf) and word[:-2] in self.word_list:
                    return [word[:-2],"كثير"]
        return []
    
    def extra_feminine(self,word):
        if(word[-1]=='ة' and word[:-1] in self.word_list):
            return [word[:-1],"مؤنث"]
        return []
    
    def extra_ownership(self,word):
        if(word[-1]=='ي' and word[:-1] in self.word_list):
            return [word[:-1],"ملكى"]
        if(word[-1]=='ك' and word[:-1] in self.word_list):
            return [word[:-1],"ملكك"]
        return []
    
    def get_extra_words(self,word):
        ''' call all extra_ functions to get the word + extra meaning '''
        
        for method in self.extra_methods:
            output = method(word)
            if(len(output)>0):return output

        
        return []
    
