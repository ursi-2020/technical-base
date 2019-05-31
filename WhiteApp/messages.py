from threading import Thread


class AsyncMessages:
    # DATA #
    protocol: str = "http"
    host: str = "localhost"
    port: int = 5002
    name: str = None
    identifier: str = None

    # STATE #
    registered: bool = False

    def __init__(self, name, identifier, protocol: str = None, host: str = None, port: int = None) -> None:
        self.protocol = self.protocol if protocol is None else protocol
        self.host = self.host if host is None else host
        self.port = self.port if port is None else port
        self.name = name
        self.identifier = identifier

    def register(self):
        # TODO Create the queue in rabbitMQ with the given name and id
        # TODO (maybe not necessary, if channels are created as messages are sent)
        pass

    def start_reading(self, callback: function = None):
        # TODO read and handle all messages in a loop and wait for new ones to be sent from RabbitMQ
        pass

    def stop_reading(self):
        # TODO stop the reading loop from above
        pass

    def read_next_async_message(self, callback: function = None):
        # TODO read one message if it exists
        pass

    def send_async_message(self, name, identifier, callback: function = None) -> None:
        # TODO send an asynchronous message to the given name/id
        pass

    def send_async_file(self, name, identifier, callback=None):
        # TODO send an asynchronous file to the given name/id
        # TODO => create shared folder if it doesnt exist -> put file in shared folder -> send message telling where and what the file is about
        pass

    def get_url(self):
        return self.protocol + "://" + self.host + ":" + str(self.port) + "/" + self.name


class SyncRequests:
    protocol: str = "http"
    host: str = "localhost"
    port: int = 5001
    name: str = None
    identifier: str = None

    def __init__(self, name, identifier, protocol: str = None, host: str = None, port: int = None) -> None:
        self.protocol = self.protocol if protocol is None else protocol
        self.host = self.host if host is None else host
        self.port = self.port if port is None else port
        self.name = name
        self.identifier = identifier

    def register(self):
        # TODO Register to API manager with given name and identity
        pass

    def get_url(self):
        return self.protocol + "://" + self.host + ":" + str(self.port) + "/" + self.name


if __name__ == '__main__':
    exit(1)
