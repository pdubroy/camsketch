import rumps
import threading

from server import CamsketchServer

class CamsketchStatusBarApp(rumps.App):
    def __init__(self, address):
        super(CamsketchStatusBarApp, self).__init__("Camsketch")
        self.menu = [address]


if __name__ == "__main__":
    server = CamsketchServer()
    threading.Thread(target=server.serve_forever).start()
    app = CamsketchStatusBarApp(server.address)
    app.run()
    server.shutdown()
