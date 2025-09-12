import pypresence
import time
import threading

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
                details="Taking notes...",
                state="Working on a project",
                large_text="Noteted",
                start=int(time.time())
            )

            # the meow is stupid and fixes a bug
            # it would take like a soild 10 seconds to actually close the app
            # so this fixes it somehow :sob:
            for meow in range(15):
                if not self.running:
                    break
                time.sleep(1)
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
