
# GBADS Dashboard Template

A dashboard template that allows users to start building a custom GBADs theme dashboard.

## Parts of the template
These are the main parts of this template. You will probably be making most of your edits in these files:

#### [dashboard.py](https://github.com/GBADsInformatics/Dashboard_Template/blob/master/dash/flask_app/plotlydash/dashboard.py)
This file includes all the callbacks for the components in the layouts.

#### [layouts.py](https://github.com/GBADsInformatics/Dashboard_Template/blob/master/dash/layouts.py)
The page layouts are made in this file. This is where all the dash components are found. 

#### [stylecheet.css](https://github.com/GBADsInformatics/Dashboard_Template/blob/master/dash/flask_app/plotlydash/assets/stylesheet.css)
All the styling is done here. Most components already have custom CSS to go along with them but 
you can add more here.

## Build and Run Locally

Clone the project

*Contact [@Amardeep](https://github.com/amardeep-1) to add a .env file*

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd dash
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Start the application

```bash
  python3 wsgi.py
```

  
## Features
- Fullscreen mode
- Login/Logout

  
## Authors
- [@Amardeep](https://github.com/amardeep-1)
- [@Nitin](https://github.com/Nitin501)

  