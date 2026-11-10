class FileWriter:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save(self, data: str):
        with open(self.file_path, 'w') as file:
            file.write(data)