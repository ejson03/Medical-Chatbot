import uuid

class Session():
    def __init__(self):
        self.id = uuid.uuid4()
        self.vars = {
            self.id : {}
        }

    def set(self, token):
        self.vars[self.id]["token"] = token
        print(self.vars)

    def get(self):
        print(self.vars)
        return self.vars[self.id]["token"]


    def __str__(self):
        return str(self.vars[self.id])