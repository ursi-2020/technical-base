

class Writefile:
    directory_path = None

    def __init__(self, directory_path = "C:/Users/Public/"):
        self.directory_path = directory_path

    # Askip python est tres bon pour les longues string c'est pour ca que je laisse comme ca
    def write_file(self, name_file, content):
        try :
            f = open(self.directory_path + name_file, "w+")
            f.write(content)
            f.close()
        except Exception:
            print(self.directory_path + name_file + ' error, maybe bad access or directory not available')

    def append_to_file(self, name_file, content):
        try :
            f = open(self.directory_path + name_file, "a")
            f.write(content)
            f.close()
        except Exception:
            print(self.directory_path + name_file + ' not found')

    def read_file(self, name_file):
        try :
            f = open(self.directory_path + name_file, "r")
            contents = f.read()
            f.close()
            return contents
        except Exception:
            print(self.directory_path + name_file + ' not found')