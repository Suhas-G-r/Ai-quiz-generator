# AI Quiz App

A modern, responsive, and dynamic quiz application powered by **Google Gemini AI**. It allows users to dynamically generate customizable quizzes on any topic, play them, review detailed explanations for answers, and track their performance over time on an analytics dashboard.

---

### 🚀 Tech Stack

- **Backend**: Python 🐍 + Flask 🌐
- **AI Engine**: Google Gemini API (`gemini-2.5-flash`) 🤖
- **Database**: SQLite 🗃️ (Automatic migrations)
- **Frontend**: Custom HSL gradients, Tailwind CSS, Bootstrap 🎨🅱️, and Chart.js 📈

---

### 📦 Installation & Setup

To run this project locally, follow these simple steps:

#### 1. Obtain a Google Gemini API Key
- Go to [Google AI Studio](https://aistudio.google.com/).
- Generate an API key.

#### 2. Configure Environment Variables
- Create a file named `.env` in the project root directory.
- Add your API key as follows:
  ```env
  API_KEY=your_actual_gemini_api_key_here
  ```

#### 3. Set Up Python Virtual Environment
Create and activate a virtual environment for the project:
```sh
# On Windows:
python -m venv venv
venv\Scripts\activate

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

#### 4. Install Dependencies
Install the required packages:
```sh
pip install -r requirements.txt
```

#### 5. Run the Application
Start the Flask application (database migrations run automatically on startup):
```sh
python app.py
```

#### 6. Access the Application
Open your web browser and go to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

### 🌟 Meet the Developer

<p align="center">
  <a href="https://github.com/Suhas-G-r" target="_blank">
    <img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Profile" />
  </a>
</p>
