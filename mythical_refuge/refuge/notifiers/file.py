class FileNotifier:
    def __init__(self, path: str = "mirror_log.txt"):
        self.filepath = path

    def notify(self, message: str):
        with open(self.filepath, "a", encoding="utf-8") as file:
            file.write(message + "\n")
