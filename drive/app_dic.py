# Dictionary who register each app and the path where the files
# will be sent
app_dict = {
    "app": ("path", "route")
}

# Queue des message sent
message_sent_queue = []

was_get = False


def get_was_get():
    return was_get


def set_was_get_to_true():
    was_get = True


def add_app_to_dict(app, path, route):
    app_dict[app] = (path, route)


def get_path(app):
    return app_dict[app][0]


def get_route(app):
    return app_dict[app][1]


def append_queue(app_name, path, name_file):
    message_sent_queue.append((app_name, path, name_file))


def queue_pop():
    if message_sent_queue:
        return message_sent_queue.pop(0)
    else:
        return False, False, False
