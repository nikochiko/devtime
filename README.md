# DevTime - Code-time metrics for developers 👨‍💻
🕒 We track time for you while you do the coding. Available at [DevTime.Tech](http://devtime.tech)

## Development Setup

### Techstack
The main server is a Flask app - designed so to keep it small and lightweight. The production database
is a PostgreSQL DB on Heroku, although the app is configured to run with SQLite without any additional
dependencies (especially useful for development environments). 

### Cloning the Repo

To get the repository on your local device, install git and run:

```git
git clone https://github.com/nikochiko/devtickticktick.git
```

### [For the server] Get the server running

1. Make changes in the app/config.py file and edit the Auth0 keys as per your app.
Create the app on [Auth0](https://auth0.com). You'll also have to create a GitHub OAuth
app, and connect it from the Auth0 connections dashboard.

2. Navigate to `server/` directory in the terminal and install the dependencies.

```shell
cd server/

# optional: install and setup virtualenv
python3 -m venv venv/  # this sets up a virtual environment in venv/ directory
source venv/bin/activate  # activate that venv. use `deactivate` to exit it later

python3 -m pip install -r requirements.txt
```

3. Copy `.env.example` to `.env`. This is where we'll keep top-level configuration.
Saves us the hassle of going into editing code every time we change something. This is
especially useful to store config variables that are sensitive (api-keys, secrets).
For example, on Linux:

```shell
cp .env.example .env
 ```

4. Now run the server with Flask

```shell
flask run -h 0.0.0.0 -p 8000
```

Now go to your browser and head to http://localhost:8000 to see the website in action.

## Roadmap

### The project currently has:
* Authentication setup with GitHub OAuth via Auth0
* API-Key functionality
* Ability to receive heartbeats from editors and store them as coding sessions in the database

### What we want it to have in the future:
* [ ] Better UI/UX
* [ ] Coding charts - hourly, daily, weekly
* [ ] Widgets of these charts for showing on Portfolios
* [ ] Widget for whether the user is currently coding/idle/offline
* [ ] Editor plug-ins
