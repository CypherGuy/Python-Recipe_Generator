# PantryPal - AI-Powered Recipe Generator

## Introduction

**PantryPal** is a **Docker and Azure-hosted** AI-powered recipe generator that allows users to create and discover recipes based on filters, preferences, and recently generated recipes. The system is built using **Streamlit**, **MySQL**, and **LangChain**, with OpenAI integration for intelligent recipe recommendations. The app is deployed using **Azure Container Instances** with **Nginx** as a reverse proxy.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Docker Deployment](#docker-deployment)
- [Azure Hosting](#azure-hosting)
- [Database Structure](#database-structure)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Features

- **User Authentication**: Secure login and signup using MySQL.
- **AI Recipe Generation**: Powered by **LangChain** and **OpenAI** APIs.
- **Recent Recipes**: View recently generated and community-contributed recipes.
- **Filter System**: Search and filter recipes based on user-defined criteria.
- **Scalable Deployment**: Hosted on **Azure Container Instances** with **Nginx**.
- **Secure Access**: Reverse proxy and SSL support via **Nginx**.

## Project Structure

```
PantryPal/
│── project_contents/
│   ├── app/
│   │   ├── app.py             # Main entry point for the application
│   │   ├── pages/
│   │   │   ├── login.py       # Handles user authentication
│   │   │   ├── signup.py      # Handles new user registration
│   │   │   ├── recipe.py      # AI-powered recipe generation logic
│   │   │   ├── view_recents.py# Displays recent community recipes
│── deployment.yml              # Azure deployment configuration
│── Dockerfile                  # Docker build instructions
│── nginx.conf                   # Nginx reverse proxy configuration
│── environment.yml              # Conda environment dependencies
│── run.sh                       # Script to start Nginx and Streamlit
│── README.md                    # Project documentation
```

## Installation

### Prerequisites

- **Python 3.11** (as specified in `environment.yml`)
- **Docker**
- **Azure CLI** (for deployment)
- **MySQL Database**

### Steps

1. Clone the repository:
```bash
   git clone https://github.com/your-username/PantryPal.git
   cd PantryPal
  ```
2. Install dependencies:

```bash
conda env create -f environment.yml
conda activate pantrypal
```
3. Set up environment variables in .env:

```bash
DATABASE_PASSWORD_LOGINS=your_password
DATABASE_PASSWORD_RECIPES=your_password
SERPER_API_KEY=your_api_key
OPENAI_API_KEY=your_openai_key
```
4. Run the application locally:

```bash
streamlit run project_contents/app/app.py
```
## Configuration

## Environment Variables

Stored in `.env` file:

```
DATABASE_PASSWORD_LOGINS
DATABASE_PASSWORD_RECIPES
SERPER_API_KEY
OPENAI_API_KEY
```

### Database Structure

- **Users Table** (for authentication)
- **Recipes Table** (for storing generated recipes)
- **Filters Table** (for storing user-defined filters)

## Docker Deployment

1. Build the Docker image:  
```
docker build -t pantrypal .
```
2. Run the container:
   
```
docker run -p 80:80 -p 443:443 --env-file .env pantrypal
```
## Azure Hosting

### Steps to Deploy

1. Build and push the image to Azure Container Registry:  
```az acr build --image pantrypal:v1 --registry pantrypalregistry.azurecr.io```

2. Deploy to Azure Container Instances:  
```az container create --resource-group PantryPalGroup --name PantryPal --image pantrypalregistry.azurecr.io/pantrypal:v1 --dns-name-label pantrypal --ports 80 443```

3. Check deployment logs:  
```az container logs --name PantryPal --resource-group PantryPalGroup```

## Nginx Reverse Proxy

The `nginx.conf` file configures **Nginx** as a reverse proxy to forward traffic to the Streamlit application.

Key Configuration:

```server { server_name pantrypal.uksouth.azurecontainer.io; location / { proxy_pass http://127.0.0.1:8501/; } location ^~ /static { proxy_pass http://127.0.0.1:8501/static/; } }```

To manually start Nginx and the app, run:  
```bash run.sh```


## Dependencies

- Python 3.11
- Streamlit
- MySQL Connector
- LangChain
- OpenAI API
- Google Serper API
- Streamlit Extras
- Nginx (for reverse proxy)

## Troubleshooting

- **Streamlit not running?** Ensure all dependencies are installed and environment variables are set correctly.
- **Database connection issues?** Verify MySQL is running and credentials are correct.
- **Docker build failure?** Ensure Docker is installed and running.

## Contributors

- **[Me](https://github.com/CypherGuy)** – *Solo developer*

## License

This project is licensed under the **MIT License**.
