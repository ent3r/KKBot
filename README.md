# KKBot

This is the repository used for hosting the code of the KKBot discord bot.

![Heroku](https://heroku-badge.herokuapp.com/?app=discord-bot-kodeklubben)

## About

This bot was made by using the [`discord`](https://pypi.org/project/discord/) python library, which is actually just a mirror of the [`discord.py`](https://github.com/Rapptz/discord.py) library. The [`discord.py`](https://github.com/Rapptz/discord.py) library is a wrapper for the discord API.

## Requirements

There are two ways to install the needed requirements for this project. The reccomended way is to use `pipenv`, as `pip` is going to go away, but both are supported.

### Using `pip`

To use this method you need to make sure you have `pip` installed. To install `pip` you can follow [this](https://pip.pypa.io/en/stable/installing/) tutorial.

This command will install all requirements listed in `requirements.txt`

```bash
pip install -r requirements.txt
```

### Using `pipenv`

[`Pipenv`](https://github.com/pypa/pipenv) is the new package manager made py pypa, the same people that made `pip`

This command will make sure the packages listed in `pipfile.lock` are installed.

```bash
pipenv sync
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md), and [STRUCTURE.md](./STRUCTURE.md)
