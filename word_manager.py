import random
import secrets
from pathlib import Path

class WordManager:
    def __init__(self, word_file="words.txt"):
        self.word_file = word_file
        self.word_list = self.load_words()
        
    def load_words(self):
        """Load words from the words.txt file in the same folder as the app"""
        if not Path(self.word_file).exists():
            raise FileNotFoundError(
                f"{self.word_file} not found!\n\n"
                "Please create a 'words.txt' file in the same directory as the application.\n"
                "The file should contain at least 5000 words, one per line.\n\n"
                "You can download word lists from:\n"
                "- https://github.com/dwyl/english-words\n"
                "- https://www.mit.edu/~ecprice/wordlist.10000"
            )
        
        try:
            with open(self.word_file, 'r', encoding='utf-8') as file:
                words = [line.strip() for line in file if line.strip()]
                
            print(f"Loaded {len(words)} words from {self.word_file}")
            
            return words
            
        except Exception as e:
            raise Exception(f"Problem reading {self.word_file}: {e}")
    
    def get_random_words(self, count):
        if not self.word_list:
            raise Exception("No words available! Please check words.txt file.")
        
        if count > len(self.word_list):
            raise Exception(f"Asked for {count} words but only {len(self.word_list)} available.")
        
        return [secrets.choice(self.word_list) for _ in range(count)]
    
    def get_word_count(self):
        return len(self.word_list)