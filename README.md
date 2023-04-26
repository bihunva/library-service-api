## Library Management System

<p>RESTful API service that provides functionality for managing a library's book borrowing system.</p>

___

### Technologies Used

<p>The library management system is built using Python and Django Rest Framework for the back-end development and user interface. PostgreSQL is used for the database management. Redis and Celery are used as the asynchronous task queue to manage background tasks. The system is containerized using Docker, and Stripe is used as the payment processing platform.</p>

___

### Features

The system offers the following features:
<ul>
<li>Book management: add new books to the system, update book information, and track availability.</li>
<li>Borrowing management: check out books to users, set due dates, and track borrowing history.</li>
<li>User management: add new users, update user information, and track borrowing history.</li>
<li>Payment management: track payments made by users, generate payment reports.</li>
<li>Notification management: send automated notifications to library managers telegram chat about upcoming due dates</li>
</ul>

___

### Getting started

<p><i>The project can be installed locally or using Docker</i></p>

##### Installation using Docker

<p>Before you begin, make sure you have Docker installed on your computer. To do this, run the following command:</p>

```shell
docker --version
```

<p>The result of the execution should be the docker version. If it is not, install docker on your computer, if everything is ok, follow these steps:</p>

1. Clone the project repository to your computer using the following command:
    ```shell
    git clone https://github.com/bihunva/library-service-api.git
    ```

2. Add the <strong>.env</strong> file to the root of the project. In this file you must specify the values of the
   environment variables, an example is in the file <strong>.env.sample</strong>.


3. Build Docker images by running the following command:
   ```shell
   docker-compose build
   ```

4. Run Docker containers by running the following command:
   ```shell
   docker-compose up
   ```

##### Local installation

<p>Before you begin, make sure you have Python and PostgreSQL installed on your computer. To do this, run the following commands:</p>

```shell
python3 --version
```

```shell
psql --version 
```

<p>The command output should be Python and PostgreSQL versions, respectively. If it is not, you need to install Python and PostgreSQL on your computer. If everything is ok, follow these steps:</p>

1. Clone the repository:
    ```shell
    git clone https://github.com/bihunva/library-service-api.git
    ```

2. Create and activate a virtual environment (venv):
    ```shell
    python3 -m venv venv
    source venv/bin/activate # for Unix-based systems
    venv\Scripts\activate # for Windows
    ```

3. Install dependencies:
    ```shell
    pip install -r requirements.txt
    ```

4. Set the following environment variables with your own values in a .env file in the root directory of the project:

   ```
   POSTGRES_DB=<POSTGRES_DB>
   POSTGRES_USER=<POSTGRES_USER>
   POSTGRES_PASSWORD=<POSTGRES_PASSWORD>
   POSTGRES_HOST=<POSTGRES_HOST>
   POSTGRES_PORT=<POSTGRES_PORT>
   TELEGRAM_BOT_TOKEN=<TELEGRAM_BOT_TOKEN>
   TELEGRAM_CHAT_ID=<TELEGRAM_CHAT_ID>
   CELERY_BROKER_URL=<CELERY_BROKER_URL>
   CELERY_RESULT_BACKEND=<CELERY_RESULT_BACKEND>
   STRIPE_SECRET_KEY=<STRIPE_SECRET_KEY>
   STRIPE_PUBLISHABLE_KEY=<STRIPE_PUBLISHABLE_KEY>
   ```

5. Run migrations
    ```shell
   python manage.py migrate
    ```

6. Start the development server
    ```shell
    python manage.py runserver
    ```

7. Start Celery worker
    ```shell
    celery -A config worker -l info
    ```

8. Start Celery Beat
    ```shell
    celery -A config beat -l info
    ```

Now, you should be able to access the development server at http://localhost:8000/.
