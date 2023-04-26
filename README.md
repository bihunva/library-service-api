## Library Management System

<p>RESTful API service that provides functionality for managing a library's book borrowing system.</p>

### Installation



### Features

The system offers the following features:
<ul>
<li>
Book management: add new books to the system, update book information, and track availability.
</li>
<li>
Borrowing management: check out books to users, set due dates, and track borrowing history.
</li>
<li>
User management: add new users, update user information, and track borrowing history.
</li>
<li>
Payment management: track payments made by users, generate payment reports.
</li>
<li>
Notification management: send automated notifications to library managers telegram chat about upcoming due dates
</li>
</ul>

### Technologies Used
<p>The library management system is built using Python and Django Rest Framework for the back-end development and user interface. PostgreSQL is used for the database management. Redis and Celery are used as the asynchronous task queue to manage background tasks. The system is containerized using Docker, and Stripe is used as the payment processing platform.</p>
