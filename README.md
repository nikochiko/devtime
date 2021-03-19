# devtickticktick
Dev tick tick tick. &lt;secret!>

## Development Setup

* Cloning the Repo

To get the repository on your local device, install git and run:

```git
git clone https://github.com/nikochiko/devtickticktick.git
```

* [For the server] Get the server running

    1. Make changes in the app/config.py file and edit the Auth0 keys as per your app.
    Create the app on [Auth0](https://auth0.com). You'll also have to create a GitHub OAuth
    app, and connect it from the Auth0 connections dashboard.

    2. Enter `server/` directory and copy `.env.example` to `.env`
    For example, on Linux:

    ```bash
    $ cp .env.example .env
    ```

    3. Now run the server with Flask
    
    ```shell
    $ flask run -h 0.0.0.0 -p 8080
    ```

    Now go to your browser and head to http://0.0.0.0/8080 to see the website in action.
