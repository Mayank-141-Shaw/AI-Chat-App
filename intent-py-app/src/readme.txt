1. Start the virtual env first
    --> create a virtual env if not exists ==> py -m venv env_name
    --> inside chatbot/env_name folder -- Scripts\activate in cmd
    this will start the env

2. Install some requirements 
    --> pip install -r requirements.txt

    To save your packages installed --> pip freeze > requirements.txt

3. If debugging problem create a .env file in the /src folder and add FLASK_ENV=development

4. if running problem use py app.py   or   flask run