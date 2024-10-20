# Weather App
- Project views the different weather conditions for the selected cities.
- It takes the cities and using the weather API provided, fetches the data.
- Enables to add multiple cities of user wish.
- Takes the weather data for every 10 mins from the API.
- Once in a Day i.e. at 11:55 PM it collects the aggregates of the day and stores them.
- Can visualise  graphically The Day Wise Analysis of each and every city.
- Can add and view alerts which you will get notified on the home screen. 

## Design Parameters
- Tech Stack -> Python, Django, REST framework, HTML, Bootstrap, JavaScript, APScheduler.
- I followed Django’s app-based structure, dividing the code into separate apps for better maintainability and scalability.
- Added a folder Jobs to schedule the API calls periodically.
- The project adheres to the MVC pattern to clearly separate business logic from the user interface.
- Used Advanced Python Scheduler (APScheduler) for scheduling the API calls every 10 mins and once a day for daily aggregates.
- I have used PostgreSQL as my Database for local machine. To make installation easy, I have changed it to SQLite.
- Populates the database every 10 mins for Weather Data and once a day for Daily Aggregates.

## Build Instructions for windows
- Clone the repository and ...
- Create and Activate virtual environment
  - Open the forlder.
  - ``` bash
     python -m venv venv
    ```
  - ``` bash
      cd venv\Script\activate
    ```
- Install requirements
  - ``` bash
      pip install -r requirements.txt
    ```
- Run the App
  - ``` bash
    python manage.py makemigrations
    ```
  - ``` bash
     python manage.py migrate
    ```
  - ``` bash
     python manage.py runserver
    ```
  - Navigate to the Link and view the website.
