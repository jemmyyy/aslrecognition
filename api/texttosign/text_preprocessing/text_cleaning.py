# problems 
# - fix the probelm of ة and ه
import re

class Transformer:
    ''' this class contains multiple methods & transformation applied on the text '''
    replaced_letters_dic = {
        "ة":"ه", #  convert ه to ة
        "أ":"ا",
        "آ":"ا",
        "اّ":"ا",
        "إ":"ا",
        "ى":"ي"
    }
    
    def remove_duplications(text):
        p_longation = re.compile(r'(.)\1+')
        subst = r"\1\1"
        text = text.replace("\n"," ")
        text = re.sub(p_longation, subst, text)
        text = text.strip().replace("  "," ")
        
        text = text.replace('وو', 'و')
        text = text.replace('يي', 'ي')
        text = text.replace('اا', 'ا')
        
        return text
    
    def replace_letters(text):
        # convert list to string to apply the next operations
        
        for key,value in Transformer.replaced_letters_dic.items():
            text = text.replace(key,value)
        
        return text

            
    def pipeline(text,view=False):
        text = Transformer.remove_duplications(text)
        text = Transformer.replace_letters(text)
        final =  text.split(" ")
        
        if view:
            for i, word in enumerate(final):
                final[i] = word
            print("after text cleaning ",word)
        return final
