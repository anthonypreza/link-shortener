# link-shortener

A web application for shortening URLs. The server uses FastAPI for all API logic and SQLModel for storing the link data. A simple HTML form handles posting the long URL to the server, which responds by rendering a shortened version. Navigating to the shortened link redirects to the long URL. Styling is done by Bootstrap. This project was built quickly mainly for exploring SQLModel + FastAPI together.

You can run the application quickly via Docker:

```bash
docker build -t link-shortener .
docker run -d -p 8000:80 link-shortener
```

The app will be available on your local machine on port 8000. You can also run the app with Uvicorn:

```
python -mvenv .venv
.venv/bin/pip install -rrequirements.txt
.venv/bin/uvicorn server.app:app --reload
```
