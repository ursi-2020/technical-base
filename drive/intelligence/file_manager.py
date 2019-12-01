import shutil
import requests
from datetime import datetime

def extension(str):
    res = str.split('.')
    if (len(res) > 1) :
        return res[-1]
    return ""

def write(name_sender, path_file_sender, name_file, receiver):
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y-%H-%M")
    path_to_send = receiver.path_folder + "/" + name_file + timestampStr + extension(path_file_sender)
    fichier = open("/tmp/log_drive.txt", "a")
    try:
        shutil.copyfile(path_file_sender, path_to_send)
        print("File copied successfully.")
        fichier.write("File copied successfully at " + path_to_send + "from" + path_file_sender)
        # If source and destination are same
    except shutil.SameFileError:
        fichier.close()
        print("Source and destination represents the same file.")
        fichier.write("Source and destination represents the same file." + path_to_send)

        # If destination is a directory.
    except IsADirectoryError:
        fichier.close()
        print("Destination is a directory.")
        fichier.write("Destination is a directory.")

        # If there is any permission issue
    except PermissionError:
        fichier.close()
        print("Permission denied.")
        fichier.write("Permission denied.")


        # For other errors
    except:
        fichier.close()
        print("Error occurred while copying file.")
        fichier.write("Error occurred while copying file.")

    r = requests.post(receiver.route, data={'path': path_to_send, 'app': name_sender})
    fichier.close()
    return True
