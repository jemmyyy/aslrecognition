class Signs:
    ''' this class is responsible of getting the signs '''
    def __init__(self,word_dic, letters_dic):
        self.word_dic = word_dic
        self.letters_dic = letters_dic 
    
    
    def get_letters(self,lis,view=False):
        final = []
        for word in lis:
            
            if word in self.word_dic:
                final.append(word)
                continue
                
            if(len(final)>1 and (len(final[-1])==1 and final[-1]!='+' and word!='+') ):
                 final.append(" ")
            for letter in word:
                final.append(letter)
                

        if(view):
            for i, word in enumerate(final):
                final[i] = word
            print("after letters ",final)
        return final


    def get_signs(self,lis,view=False):
        final =[]
        for word in lis:
            if len(word)>1:
                final.append(self.word_dic[word])
            else:
                final.append(self.letters_dic.get(word))
                
        if(view):
            for sign in final:
                print(sign)
        return final
    
    
    def pipeline(self,lis,view=False):
        lis = self.get_letters(lis,view)
        lis = self.get_signs(lis,view)
        return lis
