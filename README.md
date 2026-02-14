# 🔗 URL Shortener Service (v1.1.0)

A professional, high-performance URL shortening service built with **Django 5.x**. This project has evolved from a basic web tool into a robust, API-first application featuring secure social identity management and real-time visitor analytics.

## 🚀 Live Demo
**URL:** [https://url-shortener-0s7j.onrender.com/](https://url-shortener-0s7j.onrender.com/)

## ✨ Key Features (v1.1.0)
* **RESTful API Engine**: Fully integrated API endpoints for link management via **Django REST Framework**.
* **Interactive API Documentation**: Embedded **Swagger UI** (OpenAPI 3.0) for live testing and programmatic exploration.
* **Class-Based Architecture (CBV)**: Migrated the entire codebase from FBVs to **Class-Based Views**, ensuring superior maintainability and adherence to Django best practices.
* **Social-Only Authentication**: Enforced secure one-tap login via **Google and Facebook**; traditional registration forms are disabled to prevent spam and ensure verified user identity.
* **Advanced Visitor Analytics**: Real-time tracking for every short link:
    * **Click Count**: Real-time increment for every successful redirect.
    * **Accurate IP Tracking**: Optimized for Render deployment using `HTTP_X_FORWARDED_FOR` headers.
    * **User-Agent Metadata**: Full browser and device identification for traffic analysis.

## 🛠️ Technical Stack
* **Framework**: Django 5.x (Python 3.13+)
* **API Documentation**: drf-spectacular
* **Database**: PostgreSQL (Production) / SQLite (Development)
* **Auth Backend**: django-allauth (OAuth2)
* **Deployment**: Render (Gunicorn + WhiteNoise)

## ⚙️ Local Development
1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/zak-liu/url-shortener.git](https://github.com/zak-liu/url-shortener.git)
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Environment Variables**: Setup a `.env` file with `DATABASE_URL`, `SECRET_KEY`, and OAuth credentials.
4.  **Run migrations and start server**:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## 🔒 API Documentation & Usage
Access the interactive documentation to explore and test endpoints:
* **Swagger UI**: `/api/docs/`
* **Example POST Request**:
    ```json
    {
      "original_url": "[https://www.google.com](https://www.google.com)"
    }
    ```
* **Authentication**: Supports **Basic Auth** (username/password) and **Session Auth** (browser login).

## 👨‍💻 Author
**Zak Liu**
