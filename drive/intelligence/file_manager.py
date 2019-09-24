from datetime import datetime
from drive.app_dic import get_path, append_queue

class File_manager():
    def __init__(self, app, path):
        self.app = app
        self.path_to_read = path

    def write_to_distant(self, content):
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S-%f)")
        path_dest = get_path(self.app) + "_" + timestampStr
        f = open(path_dest)
        f.write(content)
        f.close()
        append_queue(self.app, path_dest)
        return False

    def write(self):
        try:
            f = open(self.path_to_read, "w+")
            content = f.read()
            f.close()
            return write_to_distant(content)
        except Exception:
            print(self.path_to_read + ' error, maybe bad access or directory not available')
            return False
