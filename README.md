# devtickticktick
Dev tick tick tick. &lt;secret!>

## Development Setup

* Cloning the Repo

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
pip install virtualenv  # this installs the package you'll need to create virtualenvs
python -m venv venv/  # this sets up a virtualenv in venv/ directory
source venv/bin/activate  # activate that virtualenv. use `deactivate` to exit the virtualenv

python -m pip install -r requirements.txt
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
flask run -h 0.0.0.0 -p 8080
```

Now go to your browser and head to http://0.0.0.0/8080 to see the website in action.
