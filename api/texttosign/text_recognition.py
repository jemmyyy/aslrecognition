from .text_preprocessing.translation import Translation
from .text_preprocessing.signs import Signs
from .text_preprocessing.text_cleaning import Transformer
from .utils import load_data

class TextToSign():
    def __init__(self, avatar):

        if not avatar:
            words_file_name = "data/words.json"
            letters_file_name = "data/letters.json"
        else:
            words_file_name = "data/avatar_words.json"
            letters_file_name = "data/avatar_letters.json"
        
        conversion_file_name = "data/preprocessing.json"
        
        self.__words_dict = load_data(words_file_name)
        self.__letters_dict = load_data(letters_file_name)
        self.__conversion_dict = load_data(conversion_file_name)

        self.__translation = Translation(self.__words_dict)
        self.__sign_obj = Signs(self.__words_dict, self.__letters_dict)
    
    def __text_preprocessing(self,text):
        # Iterate through the dictionary and perform replacements
        for old_word, new_word in self.__conversion_dict.items():
            text = text.replace(old_word, new_word)
        text = Transformer.pipeline(text, view= True)
        text = self.__translation.translate(text)
        text = " ".join(text)
        for old_word, new_word in self.__conversion_dict.items():
            text = text.replace(old_word, new_word)
        text = text.split(" ")
        text = self.__sign_obj.pipeline(text, view= True)
        return text

    def text_recognition(self, text):
        text = self.__text_preprocessing(text)
        return text
    

