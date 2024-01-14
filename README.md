# Ecommerce Store

Welcome to the Ecommerce Store project! This comprehensive e-commerce solution allows you to set up an online shop for various products. It includes essential features such as a robust login system, profile management, secure payment processing (if using Stripe), a comprehensive product system, size and availability tracking, photo uploads, and an intuitive cart system. This project is production-ready, covering all the essential user needs and even some advanced features.

## Project Overview

With the Ecommerce Store project, you get:

- User-friendly product browsing and category filtering
- Detailed product pages including sizes and availability
- Convenient cart management (add, remove items)
- Comprehensive user profiles and order tracking
- Flash messages for smooth user experience
- Pagination and form handling
- Efficient caching and delayed task handling
- Admin panel for easy product and category management
- Users can also leave reviews on products to share their experiences with others.


## Technologies Used

The project leverages a powerful tech stack to ensure seamless functionality:

- Backend: Python & Django
- Database: PostgreSQL
- Caching: Redis
- Task Queue: Celery
- Frontend: HTML, CSS, JavaScript
- Web Server: Nginx
- Application Server: Gunicorn

## Challenges Faced and Future Features

During development, challenges included implementing a size system for products because of multiple many-to-many db relationshops and configuring deployment environments. Future features could include:

- Wishlist functionality
- Advanced search and filtering
- Enhanced user profile customization

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python (version x.x)
- Pip (to install project dependencies)
- [Stripe](https://stripe.com) Account (if using Stripe for payments):
  - `STRIPE_PUBLIC_KEY`: Obtain from your Stripe account dashboard.
  - `STRIPE_SECRET_KEY`: Obtain from your Stripe account dashboard.
  - `STRIPE_WEBHOOK_SECRET`: Create in your Stripe account settings.

## Installation and Setup

Follow these steps to run the project on your local machine:

1. Clone the repository and create a `media` directory at the project root.
2. Create a virtual environment: `python3 -m venv venv` and activate it: `source venv/bin/activate`.
3. Install required packages: `pip install -r requirements.txt`.
4. Install Redis, PostgreSQL, and Celery.
5. Create a PostgreSQL database and user with the necessary privileges.
6. Create a `.env` file as per the provided template with your configuration settings, including the Stripe keys and webhook secret if necessary.
7. Apply migrations: `python manage.py migrate`.
8. Start the Celery worker: `celery -A ecommerce_store worker -l info`.
9. Run the development server: `python manage.py runserver`.

## Deployment

I've successfully deployed this project using Gunicorn and Nginx on an Ubuntu server. The website domain is [fartanovprojects.space](http://fartanovprojects.space). If you want to deploy the project, especially on Ubuntu, you can rely on my deploying configurations described in the `gunicorn_conf.md` and `nginx_conf.md` files.

## Usage

Once set up, follow these steps to navigate the project:

1. Create a superuser: `python manage.py createsuperuser` to access the admin panel.
2. Access the admin panel via the web interface or `127.0.0.1/admin`.
3. Manage categories, products, sizes, images, and reviews in the admin panel.
4. Explore the website as a regular user, add products to your cart, manage your profile, and proceed to checkout.

**License:** This project is licensed under the [MIT License](LICENSE).
