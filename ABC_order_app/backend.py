import os

def filename_cleanup(filename):
    filename = filename.lower()

    if not filename.endswith('.txt'):
        filename += '.txt'
    
    return filename
    
class FileManager:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        
        # Dictionary to hold { "filename.txt": WordManagerObject }
        self.word_managers = {} 
        
        # Load existing files
        for f in os.listdir(folder_path):
            full_path = os.path.join(folder_path, f)
            if os.path.isfile(full_path):
                clean_name = filename_cleanup(f)
                # We load the file into a WordManager immediately
                self.word_managers[clean_name] = WordManager(full_path)
    
    def get_filenames(self):
        # We take the keys from the dictionary and turn them into a sorted list
        return sorted(list(self.word_managers.keys()))
    
    def add_file(self, filename, content=""):
        filename = filename_cleanup(filename)
        full_path = os.path.join(self.folder_path, filename)

        # Check the dictionary keys instead of a list
        if filename not in self.word_managers.keys():
            # 1. Physical Create
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # 2. Add a new WordManager object to our dictionary
            self.word_managers[filename] = WordManager(full_path)
            return True 
            
        return False

    def remove_file(self,filename):
        
        filename = filename_cleanup(filename)

        full_path = os.path.join(self.folder_path, filename)

        if filename not in self.word_managers.keys():
            return False 
        
        try:
            os.remove(full_path)
            del self.word_managers[filename]
            return True 
        
        except FileNotFoundError:
            # This handles the case where the file was deleted while running manually
            del self.word_managers[filename]
            return False
    
    def rename_file(self, old_name, new_name):
        old_name = filename_cleanup(old_name)
        new_name = filename_cleanup(new_name)

        # Safety Check: Old must exist, New must not exist
        if old_name not in self.word_managers or new_name in self.word_managers:
            return False

        old_path = os.path.join(self.folder_path, old_name)
        new_path = os.path.join(self.folder_path, new_name)

        try:
            # 1. Physical rename on the disk
            os.rename(old_path, new_path)
            
            # 2. Grab the existing manager from the old key
            manager = self.word_managers.pop(old_name)
            
            # 3. Update the manager's internal filename so it knows where to save later
            manager.filename = new_path
            
            # 4. Put it back into the dictionary under the new name
            self.word_managers[new_name] = manager
            
            return True
        except Exception:
            # If the OS blocks the rename (file in use, etc.), return False
            return False
        
    def save_all(self):
        for name, manager in self.word_managers.items():
            manager.save()



class WordManager:
    def __init__(self,full_file_name):

        with open(full_file_name, 'r', encoding='utf-8') as file:
            self.words = [line.strip() for line in file if line.strip()]
        
        self.words.sort()        
        self.filename = full_file_name

    def get_words(self):
        return self.words
    
    def get_filename(self):
        return self.filename
    
    def get_filename_words(self):
        return self.filename,self.words
    
    def add_word(self,new_word):
        if new_word not in self.words:
            self.words.append(new_word)
            self.words.sort()
            return True
        return False

    def remove_word(self,word):
        if word in self.words:
            self.words.remove(word)
            return True
        return False
    
    def edit_word(self,new_word,old_word):
        if old_word in self.words:
            self.words.remove(old_word)
            self.words.append(new_word)
            self.words.sort()
            return True
        return False

    def save(self):
        # We join words with newlines
        content = "\n".join(self.words)
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(content + "\n") # Adding that final newline