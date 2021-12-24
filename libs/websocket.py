from websocket import create_connection


class WebSocketObj(object):
    _ws_session = None

    def __init__(self, server_address):
        self.server_address = server_address

    def __del__(self):
        self.ws_session.close()

    @property
    def ws_session(self):
        if self._ws_session is None:
            self._ws_session = create_connection(self.server_address)
        return self._ws_session

    def send_messages(self, msg):
        self.ws_session.send(msg)

    @property
    def receiver_message(self):
        return self.ws_session.recv()

    @property
    def connected_status(self):
        return


if __name__ == "__main__":
    url = "ws://kwang:8089"
    wsc = WebSocketObj(url)
    # print(wsc.send_messages())
    for i in range(1, 15):
        wsc.send_messages(str(i))
        print(wsc.receiver_message)
