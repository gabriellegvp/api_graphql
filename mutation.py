import graphene
from flask import Flask, jsonify
from flask_graphql import GraphQLView
import itertools

# Contadores de ID
user_id_counter = itertools.count(1)
task_id_counter = itertools.count(1)

# Dados simulados em memória
users = []
tasks = []

# Definição das Classes
class UserModel:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class TaskModel:
    def __init__(self, id, title, description, user):
        self.id = id
        self.title = title
        self.description = description
        self.user = user

# GraphQL Object Types
class User(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    email = graphene.String()

class Task(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    user = graphene.Field(User)

# Mutações
class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(lambda: User)

    def mutate(self, info, name, email):
        if not name.strip() or not email.strip():
            raise Exception("Nome e e-mail não podem estar vazios")

        user = UserModel(next(user_id_counter), name, email)
        users.append(user)
        return CreateUser(user=User(id=user.id, name=user.name, email=user.email))

class CreateTask(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        title = graphene.String(required=True)
        description = graphene.String(required=True)

    task = graphene.Field(lambda: Task)

    def mutate(self, info, user_id, title, description):
        user = next((u for u in users if u.id == user_id), None)
        if not user:
            raise Exception("Usuário não encontrado")

        if not title.strip() or not description.strip():
            raise Exception("Título e descrição não podem estar vazios")

        task = TaskModel(next(task_id_counter), title, description, user)
        tasks.append(task)

        return CreateTask(
            task=Task(
                id=task.id,
                title=task.title,
                description=task.description,
                user=User(id=user.id, name=user.name, email=user.email),
            )
        )

# Query
class Query(graphene.ObjectType):
    all_users = graphene.List(User)
    all_tasks = graphene.List(Task)
    user_by_id = graphene.Field(User, id=graphene.Int(required=True))
    task_by_id = graphene.Field(Task, id=graphene.Int(required=True))

    def resolve_all_users(self, info):
        return [User(id=user.id, name=user.name, email=user.email) for user in users]

    def resolve_all_tasks(self, info):
        return [
            Task(
                id=task.id,
                title=task.title,
                description=task.description,
                user=User(id=task.user.id, name=task.user.name, email=task.user.email),
            )
            for task in tasks
        ]

    def resolve_user_by_id(self, info, id):
        user = next((u for u in users if u.id == id), None)
        if not user:
            return None
        return User(id=user.id, name=user.name, email=user.email)

    def resolve_task_by_id(self, info, id):
        task = next((t for t in tasks if t.id == id), None)
        if not task:
            return None
        return Task(
            id=task.id,
            title=task.title,
            description=task.description,
            user=User(id=task.user.id, name=task.user.name, email=task.user.email),
        )

# Mutations
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_task = CreateTask.Field()

# Configuração do Schema
schema = graphene.Schema(query=Query, mutation=Mutation)

# Configuração do Flask
app = Flask(__name__)
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Ativa a interface GraphiQL para testes
    )
)

@app.route('/')
def home():
    return jsonify({"message": "Bem-vindo à API GraphQL!"})

if __name__ == "__main__":
    app.run(debug=True)