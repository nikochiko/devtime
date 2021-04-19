# DevTime - Code-time metrics for developers 👨‍💻
🕒 We track time for you while you do the coding. Available at [DevTime.Tech](http://devtime.tech)

![image](https://user-images.githubusercontent.com/37668193/115263491-19ac1e80-a153-11eb-9be6-5bccc942e2ce.png)

## How to use?

1. Sign up for DevTime on https://devtime.tech. It's still a work in progress so you might notice a few bugs
and a few incomplete views. Report them, on the issues tracker right [here](https://github.com/nikochiko/devtime/issues/new).
2. Get the DevTime extension for your editor. We have the one for VS-Code available atm - https://marketplace.visualstudio.com/items?itemName=DevTime.devtime
3. Get your API-key from the activity tab. Now when you open VS-Code, it will prompt you for this API key. Copy/paste the key there and you're good to go!!
4. Now now you can just focus on writing your code. You can go to the dashboard - https://devtime.tech/dashboard and see your activity. But hey that's not
even half of what DevTime means to become, so you keep writing your code, we'll keep adding new fun features. We'll notify you when we do 😄


## Development Setup

### Techstack
The main server is a Flask app - designed so to keep it small and lightweight. The production database
is a PostgreSQL DB on Heroku, although the app is configured to run with SQLite without any additional
dependencies (especially useful for development environments). 

### Cloning the Repo

To get the repository on your local device, install git and run:

```git
git clone https://github.com/nikochiko/devtime.git
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
* [x] Better UI/UX
* [x] Coding charts - hourly, daily, weekly

### What we want it to have in the future:
* [ ] Widgets of these charts for showing on Portfolios
* [ ] Widget for whether the user is currently coding/idle/offline
* [ ] Editor plug-ins:
  * [X] VS-Code - https://github.com/nikochiko/devtime-vscode
  * [ ] Atom
  * [ ] Sublime 
