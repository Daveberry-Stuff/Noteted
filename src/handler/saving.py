import threading
import os
import src.backend.getFromJSON as getFromJSON

class Saver:
    def __init__(self, interval=10):
        self.interval = interval
        self.timer = None
        self.running = False
        self.filePath = None
        self.contentGetter = None

    def save(self):
        if self.filePath and self.contentGetter:
            content = self.contentGetter().rstrip()
            try:
                with open(self.filePath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Saved {self.filePath}")

                base, ext = os.path.splitext(self.filePath)
                if ext:
                    filePath = base + ext
                    if not os.path.exists(filePath):
                        with open(filePath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Saved {filePath}")

            except Exception as e:
                print(f"Error saving file: {e}")

    def _save(self):
        if not self.running:
            return

        if getFromJSON.getSetting("EnableAutoSaving"):
            self.save()

        self.timer = threading.Timer(self.interval, self._save)
        self.timer.start()

    def start(self, filePath, contentGetter):
        if self.running:
            self.stop()
        
        self.filePath = filePath
        self.contentGetter = contentGetter
        self.running = True
        self._save()

    def stop(self):
        if self.timer:
            self.timer.cancel()
        self.running = False