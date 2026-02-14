# Django URL Shortener

A modern, functional URL shortening service built with Django 5.x. This project features secure third-party authentication, redirection logic, and visitor analytics.

## 🚀 Live Demo
**URL:** [https://url-shortener-0s7j.onrender.com/](https://url-shortener-0s7j.onrender.com/)

## ✨ Key Features
* **Social Authentication**: Integrated Google and Facebook Login using `django-allauth` for secure user access.
* **URL Management**: Logged-in users can create unique short codes for long destination URLs.
* **Instant Redirection**: High-performance redirection from short codes to original destination URLs.
* **Visitor Analytics**: Comprehensive tracking for each click, including:
    * **Click Count**: Total number of redirects per link.
    * **Source IP**: Captured using `HTTP_X_FORWARDED_FOR` to ensure accurate tracking behind Render's proxy/load balancer.
    * **User Agent**: Browser and device metadata for each visitor.

## 🛠️ Technical Stack
* **Framework**: Django 5.x (Python 3.13+)
* **Database**: PostgreSQL (Hosted on Render)
* **Production Server**: Gunicorn
* **Styling**: Modern UI with custom CSS and Inter/Google Fonts.

## ⚙️ Local Development
1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/zak-liu/url-shortener.git](https://github.com/zak-liu/url-shortener.git)
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Environment Variables**: Create a `.env` file or set environment variables for:
    * `DATABASE_URL`
    * `SECRET_KEY`
    * OAuth Credentials (Client ID/Secret)
4.  **Run migrations and start server**:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## 👨‍💻 Author
**Zak Liu**
