class MySet:
    def __init__(self, objects):
        self.objects = list(objects)

    def insert(self, obj):
        self.objects.append(obj)

    def find(self, obj):
        for object in self.objects:
            if object == obj:
                return True
        return False
