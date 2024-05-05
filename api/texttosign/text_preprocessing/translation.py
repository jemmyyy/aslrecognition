from .root_extraction import ArabicRoot

class Translation:
    ''' this class is responsible of translation applying final transformation on words to select the 
        correct words from the dictionary
    '''
    def __init__(self,word_dic):
        self.word_dic = word_dic
        self.arabic_root = ArabicRoot(word_dic)
        
    def translate(self,lis,view=False):
        final = []
        for word in lis:
            if word in self.word_dic:
                final.append(word)
                continue

            if(len(word)>3 and word[:2]=="ال"):
                word = word[2:]
                if word in self.word_dic:
                    final.append(word)
                    continue


            if(len(word)>=6 and word[:3]=="وال"):
                word = word[3:]
                final.append('+')
                if word in self.word_dic:
                    final.append(word)
                    continue

            output = self.arabic_root.get_extra_words(word)
            if(len(output)>0):
                final.extend(output)
                continue

            final_form = self.arabic_root.clean_word(word)
            if(final_form in self.word_dic):
                final.append(final_form)
                continue



            final.append(word)


        if(view):
            for i, word in enumerate(final):
                final[i] = word
            print("after translation ",final)
        return final
