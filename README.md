# APP

__app__.py is the main runner file for running flask server.

## Installation

Main directory contains a file requirements.txt with all the required libraries.
Other then that another file named library.txt exists which lists main packages.

```bash
pip install -r requirements.txt
```

## Run Tailwind generator

Initially tailwind css generator was used to dynamically generate css file.
This file will listen to all the changes made in all file such as html,etc inside src/.
All the generated css is stored in home_automation\static\css\main.css path file.

```bash
npm run css
```

## Routes folder contains all the python files for backend

__init__.py contains blueprint to initialize all the files and environment variables in flask server.

__config__.py fetches the supabase configuration from .env file to access and alter cloud resources. Can also config Dev environ or Production environment.

Rest details about each function can found inside each python file.
