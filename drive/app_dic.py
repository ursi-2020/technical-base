
# Dictionary who register each app and the path where the files
# will be sent
app_dict = {
    "app" : "path"
}

# Queue des message sent
message_sent_queue = []

def add_app_to_dict(app, path) :
    app_dict[app] = path

def get_path(app):
    return app_dict[app]

def append_queue(app_name, path):
    message_sent_queue.append((app_name, path))

def queue_pop():
    message_sent_queue.pop(0)
