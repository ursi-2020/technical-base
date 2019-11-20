import shutil
import requests
from datetime import datetime


def write(name_sender, path_file_sender, name_file, receiver):
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S-%f")
    path_to_send = receiver.path_folder + "/" + name_file + timestampStr
    try:
        shutil.copyfile(path_file_sender, path_to_send)
        print("File copied successfully.")

        # If source and destination are same
    except shutil.SameFileError:
        print("Source and destination represents the same file.")

        # If destination is a directory.
    except IsADirectoryError:
        print("Destination is a directory.")

        # If there is any permission issue
    except PermissionError:
        print("Permission denied.")

        # For other errors
    except:
        print("Error occurred while copying file.")

    r = requests.post(receiver.route, data={'path': path_to_send, 'app': name_sender})
    return True
