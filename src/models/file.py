class File:
    def __init__(self, name: str, size: int, path: str):
        self.name = name
        self.size = size
        self.path = path

    def __repr__(self):
        return f"File(name={self.name}, size={self.size}, path={self.path})"

    @property
    def extension(self):
        return self.name.split('.')[-1] if '.' in self.name else ''

    