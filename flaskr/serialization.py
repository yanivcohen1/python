import pickle

class MyClass2:
    def __init__(self, filename):
        self.filename = filename

    def reads(self):
        print("filename:", self.filename)

class MyClass:
    """Print and number lines in a text file."""
    def __init__(self, filename, num, obj):
        self.filename = filename
        self.lineno = num
        self.obj = obj

    def reads(self):
        print("filename:", self.filename, ", lineno:", self.lineno,
                ", class2:", self.obj.filename)

reader1 = MyClass2("my file_2")
reader2 = MyClass("my file_1", 22, MyClass2("my file_3"))

new_reader  = pickle.loads(pickle.dumps([reader1, reader2]))
for reader in new_reader:
    reader.reads()
