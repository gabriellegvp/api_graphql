import graphene
from graphene import ObjectType, String, Int, List, Field, Mutation
from data import users, tasks
from models import User, Task

# Tipos GraphQL
class UserType(ObjectType):
    id = Int()
    name = String()
    email = String()

class TaskType(ObjectType):
    id = Int()
    title = String()
    description = String()
    user = Field(UserType)

    def resolve_user(self, info):
        return next((user for user in users if user.id == self.user.id), None)

# Consultas
class Query(ObjectType):
    all_users = List(UserType)
    all_tasks = List(TaskType)
    task_by_id = Field(TaskType, id=Int(required=True))
    user_by_id = Field(UserType, id=Int(required=True))

    def resolve_all_users(self, info):
        return users

    def resolve_all_tasks(self, info):
        return tasks

    def resolve_task_by_id(self, info, id):
        return next((task for task in tasks if task.id == id), None)

    def resolve_user_by_id(self, info, id):
        return next((user for user in users if user.id == id), None)

# Mutações
class CreateUser(Mutation):
    class Arguments:
        name = String(required=True)
        email = String(required=True)

    user = Field(UserType)

    def mutate(self, info, name, email):
        if not name.strip() or not email.strip():
            raise Exception("Nome e e-mail não podem estar vazios!")

        new_id = max([u.id for u in users], default=0) + 1
        new_user = User(id=new_id, name=name, email=email)
        users.append(new_user)
        return CreateUser(user=new_user)

class CreateTask(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        user_id = Int(required=True)

    task = Field(TaskType)

    def mutate(self, info, title, description, user_id):
        if not title.strip() or not description.strip():
            raise Exception("Título e descrição não podem estar vazios!")

        user = next((user for user in users if user.id == user_id), None)
        if not user:
            raise Exception("Usuário não encontrado!")

        new_id = max([t.id for t in tasks], default=0) + 1
        new_task = Task(id=new_id, title=title, description=description, user=user)
        tasks.append(new_task)
        return CreateTask(task=new_task)

# Definindo as mutações
class Mutation(ObjectType):
    create_user = CreateUser.Field()
    create_task = CreateTask.Field()

# Schema principal
schema = graphene.Schema(query=Query, mutation=Mutation)