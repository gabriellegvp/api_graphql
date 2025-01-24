from models import User, Task

# Simulando um banco de dados em memória
users = [
    User(id=1, name="Alice", email="alice@example.com"),
    User(id=2, name="Bob", email="bob@example.com"),
]

tasks = [
    Task(id=1, title="Learn GraphQL", description="Study GraphQL basics", user_id=1),
    Task(id=2, title="Build API", description="Develop a GraphQL API with Python", user_id=1),
    Task(id=3, title="Debug API", description="Fix issues in the API", user_id=2),
]
