# A Coding Challenge(Task For Assessment) 🧑‍💻
## Todo-Management(FullStack)
# Introduction: 
#### Imagine you're writing a program for a todo-management Protected
- **This means that only you can access your Todos** and you can trust us to create Todos(***Each user can only see and delete or edit her own Todos***)
- Admin can only see users who have joined the program and see their Todos, but cannot delete or edit.

# Technology Requirements:
## Back-end 🧑‍💻
- The programming language must be **Python**.
- Use **Poetry** dependency management.
- Use **JWT** and FastAPI for this task.
- Use DataBase **Posgresql**.
- Use **Redis** for temporary data storage and using Messenger Broker.
- Send Email async (use **Celery**).
- Dockerize Project(docker-compose)
## Front-end 🏗️
- ## It would be built soon(**React**)🚧

# Run Project
- Clone project
```bash
git clone https://github.com/AliMortezaei/FullStack-TodoManagement.git
```
- Edit the .env file and specify the environment variables that are required
- Run via docker compose
```bash
docker compose up -d --build
```
- Go to browser localhost 0.0.0.0:8000

 
