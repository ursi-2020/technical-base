from datetime import datetime
from drive.app_dic import get_path, append_queue


def write_to_distant(content, app, file_name):
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S-%f")
    path_dest = get_path(app) + "/" + file_name + "_" + timestampStr
    f = open(path_dest, "w+")
    f.write(content)
    f.close()
    return False

def write(app, path, file_name):
    try:
        f = open(path, "r")
        content = f.read()
        f.close()
        return write_to_distant(content, app, file_name)
    except Exception:
        print(path + ' error, maybe bad access or directory not available')
        return False
