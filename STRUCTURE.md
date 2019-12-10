# Structure

The KKBot github is structured the following way:

```ascii
KKbot/
│
├── app/
│    ├── templates/
│    │       └ # Code for the website is in here
│    └ # Folder for entire webapp
└ # Root folder. Most of the things go in here
```

## Spesific file notes

### app/

Before editing any files in this folder, an issue should be opened to see if nessesary.

### .gitignore

This file should NOT be edited unlesss ABSOLUTELY needed

### CONTRIBUTING.md, STRUCTURE.md, README.md

Only commits from members of the repository will be accepted, as these files are kinda important.

### Pipfile, requirements.txt

These files are used for the dependencies of the project. The `requirements.txt` file is only kept for people without pipenv, and using pipenv is strongly reccomended.

### Pipfile.lock

Just don't edit this file.

### Procfile, runtime.txt

These files are used by [heroku](https://heroku.com) to setup our application and bot.

### runwebapp.py

This file is used by heroku to start the webapp. This file is REQUIRED to exist in any PR's, or they WILL get declined.

### kkbot.py

The main file of the bot. All commands go in here until further notice.
