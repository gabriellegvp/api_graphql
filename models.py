from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"

@dataclass
class Task:
    id: int
    title: str
    description: str
    user_id: int

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', user_id={self.user_id})"