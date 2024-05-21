# Custom ChatGPT - Work in Progress

Welcome, candidates! This project is a custom-built chatbot application that mimics the functionalities of ChatGPT for personal use. It's built using Python and Django for the backend, and React with Next.js for the frontend. The application offers regular chatting capabilities with history stored in the database, streaming responses, and auto-generated titles using GPT-3.5. It also allows for title editing, conversation deletion, and message regeneration. The project currently supports model selection between GPT-3.5 and GPT-4 and features a custom Django admin page for managing conversations, versions, and messages.

**Note:** This project is a work in progress, with plans to add more features and functionalities. It serves as a platform to experiment with Next.js and create a personal version of ChatGPT with custom functionalities and features.

## Technologies

### Backend
- Python
- Django
- Django Rest Framework

### Frontend
- Next.js
- React

### Database
- SQLite for now -> will be changed to PostgreSQL

## Functionalities

- Regular chatting with history stored in the database, with different versions of conversations created during message regeneration or editing.
- Streaming responses.
- Auto-generated titles using GPT-3.5.
- Title editing for given conversations.
- Deletion of conversations.
- Assistant message regeneration.
- User message editing.
- Model selection: currently GPT-3.5 or GPT-4.
- Custom Django admin page for managing conversations, versions, and messages.

## Images

### Main View
![main window](images/main_chat.png)

### Streaming
![streaming](images/streaming.png)

### Title Edition
![title edition](images/edit_chat.png)

### Switching Versions and Editing Messages
![switching versions and editing messages](images/switching_versions_editing.png)

### Login Page
![login page](images/login.png)

### Register Page
![register page](images/register.png)

### Admin Page
![admin page](images/admin.png)

## How to Run This

### Backend
1. Setup environment variables in `backend/.env` (create file if not exists):
    - `FRONTEND_URL` - URL of frontend app (default: http://127.0.0.1:3000)
    - `BACKEND_URL` - URL of backend app (default: http://127.0.0.1:8000)
    - `BE_ADMIN_EMAIL` - Email for Django admin page (default: admin@admin.com)
    - `BE_ADMIN_PASSWORD` - Password for Django admin page (default: admin)
    - `DJANGO_SECRET_KEY` - Django secret key
    - GPT settings (currently set up for Azure endpoint):
        - `OPENAI_API_TYPE`: azure
        - `OPENAI_API_BASE`: your Azure endpoint
        - `OPENAI_API_VERSION`: your Azure API version
        - `OPENAI_API_KEY`: your Azure API key
2. Create a virtual environment and install requirements from `dependencies.txt`
3. Run `python manage.py makemigrations` and `python manage.py migrate`
4. Run `python manage.py create_superuser` to create a superuser
5. Run `python manage.py create_roles` to create `user` and `assistant` roles
6. Run `python manage.py collectstatic`
7. Run `python manage.py runserver` to start the backend server
8. Alternatively, run `python server.py` to start with uvicorn

### Frontend
1. Setup environment variables in `frontend/.env.local` (create file if not exists):
    - `NEXT_PUBLIC_API_BASE_URL` - URL of backend app (default: http://127.0.0.1:8000)
2. Run `npm install`
3. Run `npm run dev` to start the frontend server

Go to `http://127.0.0.1:3000` and enjoy!