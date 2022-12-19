# Distributed DB Maker Application

BY- Utkarsh Agarwal (IMT2018082)

## Introduction:

The distributed database maker application helps us create global schemas for different databases and query on the global schema to retrieve information from the respective local databases.

The application backend is implemented in Django/Python and the frontend is made in React.js. 

Project URL - https://github.com/woolllff/Distributed_DBMS_Project.git

## Application Arch:

### Backend:

The structure of the Django application is as follows:

```bash
.
├── backend
│   ├── init.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── mainApp
│   ├── init.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── init.py
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   ├── utilities
│   │   ├── APIutil.py
│   │   ├── CLI.py
│   │   ├── init.py
│   │   ├── globalSchema.py
│   │   └── localSchema.py
│   └── views.py
├── users
│   ├── init.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── templates
│   │   └── users
│   │       └── register.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
└── db.sqlite3
```

We will keep our focus on mainApp:

- utilities
    - LocalSchema.py
        
        This file contains the class local scheme which is used to connect to the database and retrieve the metadata of the schema which we call the local schema 
        
    - GlobalSchema.py
        
        This file contains the class Global Schema which takes in the local schemas and adds the schemas from the local schema to the global one 
        
- models.py - contains the model information to be stored in the database (sqlite3)
- serializers.py - helps in making and storing the information in the database
- views.py - contains the API functions to call on URLs
- urls.py - contains the API URLs

**The details for each functions is present as comments above the function.** 

### Frontend:

The structure of the React application is as follows:

```bash
.
├── src
│   ├── App.js
│   ├── App.test.js
│   ├── CSS
│   │   └── styles.css
│   ├── components
│   │   ├── DDBApp.js
│   │   ├── createGS.js
│   │   ├── createLS.js
│   │   ├── deleteGS.js
│   │   ├── deleteLS.js
│   │   └── navbar.js
│   ├── index.js
│   ├── reportWebVitals.js
│   └── setupTests.js
├── README.md
├── package-lock.json
└── package.json
```

## Running Instructions:

Clone the repo from github

- Backend:
    - First install python3.9
    
    ```bash
    # then we need to install the virtualenv package 
    pip install virtualenv
    
    # then we need to create an environment 
    python -m venv <env name>
    # I kept <env name> as env if you want something else then update the git ignore as well 
    
    #activate the environment 
    env\Scripts\activate.bat      # this is for windows  
    env\Scripts\activate          # this is for shell
    
    #install requirements 
    pip install -r requirements.txt
    
    # update requirements 
    pip install -U -r requirements.txt
    
    #to make requirements 
    pip freeze > requirements.txt
    
    #deactivate the environment 
    deactivate
    ```
    
    - Running the application:
    
    ```bash
    # inside the backend dir 
    # make migrations for all the apps
    python manage.py makemigrations
    python manage.py makemigrations mainApp
    
    # migrate 
    python manage.py migrate
    
    #  running the server
    python manage.py runserver
    ```
    
- Frontend:
    - Installing all the packages
    
    ```bash
    #inside the frontend folder
    # this will install all the required packages from the package.json file
    npm install
    
    ```
    
    - running the frontend :
    
    ```bash
    # to run the frontend we use
    npm start 
    ```
    

## Deployment :

### Jenkins:

### Docker: