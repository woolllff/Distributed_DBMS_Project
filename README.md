# Distributed DB Maker Application

BY- Utkarsh Agarwal (IMT2018082)

## Introduction:

The distributed database maker application helps us create global schemas for different databases and query on the global schema to retrieve information from the respective local databases.

The application backend is implemented in Django/Python and the frontend is made in React.js. 

Project URL - https://github.com/woolllff/Distributed_DBMS_Project.git

## Running Instructions:

Clone the repo from GitHub

- Backend:
    - First, install python3.9
    
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
    #one more requirements for deployment 
    pip freeze > ./backend/requirements.txt
    
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

- Utilities
    - LocalSchema.py
        
        This file contains the local scheme which is used to connect to the database and retrieve the metadata of the schema which we call the local schema 
        
    - GlobalSchema.py
        
        This file contains the Global Schema which takes in the local schemas and adds the schemas from the local schema to the global one 
        
- models.py - contains the model information to be stored in the database (sqlite3)
- serializers.py - helps in making and keeping the information in the database
- views.py - contains the API functions to call on URLs
- urls.py - contains the API URLs

**************************************************************************************************The details for each function are present as comments above the functions.************************************************************************************************** 

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

## Deployment :

### Jenkins:

We use Jenkins file with git to build the project 

```
# note the file is based on windows system 

pipeline {
    environment {
    registry = "woolllff/DDBMS_APP" 
    registryCredential = 'dockerhub_id' 
    dockerImage = '' 
    }
    agent any

    stages {
        stage('Checkout'){
            steps{
                git branch: 'master', changelog: false, credentialsId: 'github_id', poll: false, url: 'https://github.com/woolllff/Distributed_DBMS_Project'
            }
        }
        stage('Build Docker'){
            steps{
                bat 'docker-compose build '
            }
        }
        
        // stage("Ansible Setup") {
        //      steps {
        //         dir('./ansible'){
        //             script{
        //                 def ansibleImage = docker.build("ansibleimage")
        //             }
        //         }
        //     }
        // }
        // stage('Ansible Deploy')
        // {
        //     steps 
        //         {
        //           bat "docker run --name ansible ansibleimage:latest"    
        //         }
        // }
    }
}

```

### Docker:

Using docker-compose to make the application

```yaml
version: "3.8"

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    networks:
      - app-network
  backend:
    build: ./backend
    ports: 
      - "8000:8000"
    networks:
      - app-network
  database:
    build: ./database
    ports:
      - "6603:3306"
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

Bellow are the docker file for the backend, frontend and database.

```docker
# docker file for backend 
FROM python:latest

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir app
COPY . ./app
WORKDIR /app

RUN cd /app
RUN pip install -r requirements.txt

EXPOSE 8000
# EXPOSE 3306
# EXPOSE 80

ENTRYPOINT ["python3" ,"manage.py", "runserver", "0.0.0.0:8000"] 

```

```docker
# docker file for frontend
FROM node:12.18.1

# RUN apt-get update 
# RUN apt-get install npm node
RUN npm install -g npm

RUN mkdir app
COPY . ./app
WORKDIR /app

RUN cd /app
RUN npm install 
EXPOSE 3000

ENTRYPOINT ["npm", "start"
```

```yaml
# The database(SQL server) docker file 
FROM mysql/mysql-server

ENV MYSQL_ROOT_PASSWORD="qwerty"
ENV MYSQL_USER="user"
ENV MYSQL_PASSWORD="pass"

COPY ./scripts/ /docker-entrypoint-initdb.d/

EXPOSE 3306
```

Using these docker files we can build the images for our backend, frontend and database 

Then we use docker-compose in our Jenkins to build the application with the frontend, backend and database 

### Azure Deployment

