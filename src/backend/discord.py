import pypresence
import time
import threading
import src.handler.path as pathHandler

class DiscordRPC:
    def __init__(self, client_id):
        self.client_id = client_id
        self.rpc = pypresence.Presence(self.client_id)
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run)
            self.thread.daemon = True
            self.thread.start()

    def run(self):
        self.rpc.connect()
        while self.running:
            self.rpc.update(
                details=pathHandler.getSetting("DiscordRPCdetails") or "Using Noteted",
                state=pathHandler.getSetting("DiscordRPCstate") or "Taking notes, as usual.",
                large_text="Noteted",
                start=int(time.time())
            )
        self.rpc.close()

    def stop(self):
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()

def startRPC(client_id):
    rpc = DiscordRPC(client_id)
    rpc.start()
    return rpc
