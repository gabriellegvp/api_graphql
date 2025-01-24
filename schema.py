import graphene
from graphene import ObjectType, String, Int, List, Field, Mutation
from data import users, tasks
from models import User, Task

# Tipos GraphQL
class UserType(graphene.ObjectType):
    id = Int()
    name = String()
    email = String()

class TaskType(graphene.ObjectType):
    id = Int()
    title = String()
    description = String()
    user = Field(UserType)

    def resolve_user(self, info):
        return next((user for user in users if user.id == self.user_id), None)

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
        new_user = User(id=len(users) + 1, name=name, email=email)
        users.append(new_user)
        return CreateUser(user=new_user)

class CreateTask(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        user_id = Int(required=True)

    task = Field(TaskType)

    def mutate(self, info, title, description, user_id):
        # Verifica se o usuário existe
        if not any(user.id == user_id for user in users):
            raise Exception("Usuário não encontrado!")

        new_task = Task(id=len(tasks) + 1, title=title, description=description, user_id=user_id)
        tasks.append(new_task)
        return CreateTask(task=new_task)

# Definindo as mutações
class Mutation(ObjectType):
    create_user = CreateUser.Field()
    create_task = CreateTask.Field()

# Schema principal
schema = graphene.Schema(query=Query, mutation=Mutation)
