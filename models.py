class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class Task:
    def __init__(self, id, title, description, user_id):
        self.id = id
        self.title = title
        self.description = description
        self.user_id = user_id
