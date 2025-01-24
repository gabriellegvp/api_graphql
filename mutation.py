import graphene
from flask import Flask, request, jsonify
from flask_graphql import GraphQLView

# Dados simulados em memória
users = []
tasks = []
user_id_counter = 1
task_id_counter = 1

# Definições das Classes
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
        global user_id_counter
        user = {
            "id": user_id_counter,
            "name": name,
            "email": email
        }
        users.append(user)
        user_id_counter += 1
        return CreateUser(user=User(**user))

class CreateTask(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        title = graphene.String(required=True)
        description = graphene.String(required=True)

    task = graphene.Field(lambda: Task)

    def mutate(self, info, user_id, title, description):
        global task_id_counter

        # Verifica se o usuário existe
        user = next((u for u in users if u["id"] == user_id), None)
        if not user:
            raise Exception("Usuário não encontrado")

        # Cria a tarefa
        task = {
            "id": task_id_counter,
            "title": title,
            "description": description,
            "user": user
        }
        tasks.append(task)
        task_id_counter += 1
        return CreateTask(task=Task(
            id=task["id"],
            title=task["title"],
            description=task["description"],
            user=User(**user)
        ))

# Query e Mutations no Schema
class Query(graphene.ObjectType):
    all_users = graphene.List(User)
    all_tasks = graphene.List(Task)

    def resolve_all_users(self, info):
        return [User(**user) for user in users]

    def resolve_all_tasks(self, info):
        return [
            Task(
                id=task["id"],
                title=task["title"],
                description=task["description"],
                user=User(**task["user"])
            )
            for task in tasks
        ]

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
        graphiql=True  # Ativa a interface GraphiQL
    )
)

@app.route('/')
def home():
    return jsonify({"message": "Bem-vindo à API GraphQL!"})

if __name__ == "__main__":
    app.run(debug=True)
