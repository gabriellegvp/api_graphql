from dataclasses import dataclass
from typing import List, Optional

@dataclass
class User:
    """
    Representa um usuário no sistema.
    """
    id: int
    name: str
    email: str

@dataclass
class Task:
    """
    Representa uma tarefa no sistema.
    """
    id: int
    title: str
    description: str
    user_id: int

class InMemoryDatabase:
    """
    Simula um banco de dados em memória para armazenar usuários e tarefas.
    """
    def __init__(self):
        self.users: List[User] = []
        self.tasks: List[Task] = []

    def add_user(self, user: User):
        """
        Adiciona um usuário ao banco de dados.
        """
        if self.get_user_by_id(user.id):
            raise ValueError(f"Usuário com ID {user.id} já existe.")
        self.users.append(user)

    def add_task(self, task: Task):
        """
        Adiciona uma tarefa ao banco de dados.
        """
        if self.get_task_by_id(task.id):
            raise ValueError(f"Tarefa com ID {task.id} já existe.")
        if not self.get_user_by_id(task.user_id):
            raise ValueError(f"Usuário com ID {task.user_id} não encontrado.")
        self.tasks.append(task)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retorna um usuário pelo ID.
        """
        return next((user for user in self.users if user.id == user_id), None)

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retorna uma tarefa pelo ID.
        """
        return next((task for task in self.tasks if task.id == task_id), None)

    def get_tasks_by_user_id(self, user_id: int) -> List[Task]:
        """
        Retorna todas as tarefas de um usuário pelo ID do usuário.
        """
        return [task for task in self.tasks if task.user_id == user_id]

# Inicializando o banco de dados em memória
db = InMemoryDatabase()

# Adicionando usuários e tarefas ao banco de dados
db.add_user(User(id=1, name="Alice", email="alice@example.com"))
db.add_user(User(id=2, name="Bob", email="bob@example.com"))

db.add_task(Task(id=1, title="Learn GraphQL", description="Study GraphQL basics", user_id=1))
db.add_task(Task(id=2, title="Build API", description="Develop a GraphQL API with Python", user_id=1))
db.add_task(Task(id=3, title="Debug API", description="Fix issues in the API", user_id=2))

# Exemplo de consultas
print(db.get_user_by_id(1))  # Retorna o usuário Alice
print(db.get_tasks_by_user_id(1))  # Retorna as tarefas de Alice