# AI Quiz Generator

A modern, responsive, and dynamic quiz application powered by **Google Gemini AI**. It allows users to dynamically generate customizable quizzes on any topic, play them, review detailed explanations for answers, and track their performance over time on an analytics dashboard.

🌐 **Live Demo**: [https://ai-quiz-generator-ftuy.onrender.com](https://ai-quiz-generator-ftuy.onrender.com)

---

### 🚀 Tech Stack

- **Backend**: Python 🐍 + Flask 🌐
- **AI Engine**: Google Gemini API (`gemini-2.5-flash`) 🤖
- **Database**: PostgreSQL 🐘 (Hosted on Neon)
- **Frontend**: Custom HSL gradients, Tailwind CSS, Bootstrap 🎨🅱️, and Chart.js 📈
- **Containerization**: Docker 🐳
- **Deployment**: Render ☁️

---

### 📦 Installation & Setup

To run this project locally using Docker, follow these simple steps:

#### 1. Obtain a Google Gemini API Key
- Go to [Google AI Studio](https://aistudio.google.com/).
- Generate an API key.

#### 2. Configure Environment Variables
- Create a file named `.env` in the project root directory.
- Add your credentials as follows:
```env
  API_KEY=your_actual_gemini_api_key_here
  DATABASE_URL=your_postgresql_connection_url_here
```

#### 3. Install Docker
- Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- Make sure Docker Desktop is running.

#### 4. Pull the Docker Image
Pull the latest image from Docker Hub:
```sh
docker pull suhas29/ai-quiz-generator
```

#### 5. Run the Application
Start the application using Docker:
```sh
docker run -p 5000:5000 --env-file .env suhas29/ai-quiz-generator python -c "from app import web_app; web_app.run(host='0.0.0.0', port=5000)"
```

#### 6. Access the Application
Open your web browser and go to:
[http://localhost:5000](http://localhost:5000)

---

### 🌟 Meet the Developer

<p align="center">
  <a href="https://github.com/Suhas-G-r" target="_blank">
    <img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Profile" />
  </a>
</p>