import rumps
import threading

import server

class CamsketchStatusBarApp(rumps.App):
    def __init__(self, address):
        super(CamsketchStatusBarApp, self).__init__("Camsketch")
        self.menu = [address]


if __name__ == "__main__":
    server.activate_camtwist()
    s = server.CamsketchServer()
    threading.Thread(target=s.serve_forever).start()
    app = CamsketchStatusBarApp(s.address)
    app.run()
    s.shutdown()
