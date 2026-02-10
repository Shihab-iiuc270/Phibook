# 📘 Phibook – Social Media Backend API

Phibook is a social media backend application built using **Django Rest Framework (DRF)**.  
It provides core social media functionalities such as creating posts, uploading images, liking posts, commenting, and secure authentication using **JWT tokens with Djoser**.

🔗 GitHub Repository: https://github.com/Shihab-iiuc270/Phibook

---

## 🚀 Features

- 🔐 JWT-based Authentication using **Djoser**
- 👤 User Registration & Login
- 📝 Create, update, and delete posts
- 🖼️ Upload images with posts
- ❤️ Like system
- 💬 Comment system
- 📦 RESTful APIs using Django REST Framework
- 📖 Interactive API documentation using **Swagger (OpenAPI)**

---

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework
- **Authentication:** Djoser + Simple JWT
- **API Documentation:** Swagger (drf-yasg)
- **Language:** Python
<!-- - **Database:** SQLite (default) -->

---

<!-- ## 📁 Project Structure

Phibook/
├── api/
│ ├── post/
│ │ ├── models.py
│ │ ├── serializers.py
│ │ ├── views.py
│ │ └── urls.py
│ ├── users/
│ └── ...
├── phibook/
├── manage.py
├── db.sqlite3
└── requirements.txt


--- -->

## 📥 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Shihab-iiuc270/Phibook.git
cd Phibook
2️⃣ Create Virtual Environment
python -m venv venv
Activate it:

venv\Scripts\activate        # Windows
source venv/bin/activate    # Linux / Mac
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Apply Migrations
python manage.py migrate
5️⃣ Run the Development Server
python manage.py runserver
Server will start at:

http://127.0.0.1:8000/
🔑 Authentication
Authentication is handled using Djoser with JWT (Simple JWT).

Users can register and log in

JWT access and refresh tokens are used

Protected APIs require a valid access token in headers

Authorization: Bearer <access_token>
📖 API Documentation (Swagger)
This project includes Swagger UI for interactive API documentation.

After running the server, open Swagger in your browser:

http://127.0.0.1:8000/swagger/
Features of Swagger:

View all available APIs

Test endpoints directly from the browser

See request/response schemas

JWT authentication support inside Swagger UI

🧱 Models Overview
Model	Description
Post	User-created post
Comment	Comment on a post
Like	Like on a post
PostImages	Images attached to a post
🧪 Testing
You can test the APIs using:

Swagger UI

DRF Browsable API

Postman / Insomnia

📌 Future Improvements
Follow / Unfollow feature

Notifications system

Pagination & filtering

Role-based permissions

Deployment (Render / Railway)

🤝 Contributing
Fork the repository

Create a new branch (git checkout -b feature-name)

Commit your changes

Push to your branch

Open a Pull Request

📄 License
This project is licensed under the MIT License

👨‍💻 Author
Mohammad Shihab Uddin
GitHub: https://github.com/Shihab-iiuc270