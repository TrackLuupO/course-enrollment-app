# Course Enrollment App

Welcome! This project is a **full-stack course enrollment application** that helps manage students, courses, and enrollments efficiently. It has a **Python backend (FastAPI + SQLAlchemy + SQLite)**, a **Vue 3 frontend**, and an optional GenAI feature for generating study tips.

Whether you're a beginner looking to learn full-stack development or an advanced developer wanting a clean, production-ready example, this guide will help you get the project running end-to-end.

---

## Why this project exists

Managing students and courses can be messy. I wanted a simple, interactive web app where you can:  
- Register students  
- Create courses  
- Enroll students in courses without allowing duplicates  
- Optionally get AI-generated study tips for each course  

Everything works **locally**, and the system is easy to set up in **VS Code**.

---

## What’s inside

**Backend (Python + FastAPI)**  
- Handles students, courses, and enrollments  
- Stores data in SQLite  
- Includes endpoints for listing students, courses, and enrollments  
- Optional `/genai/study-tips` endpoint that calls Groq’s LLaMA3 API to generate tips  

**Frontend (Vue 3 + Vite)**  
- Simple, clean UI with plain CSS  
- Pages to register students, create courses, enroll, and view study tips  
- Dropdowns are populated dynamically from the backend  

Everything is designed to **just work** after setup.

---

## Project Structure

```
- All worked dependencies worked perfectly.png
- api/
  ├── __pycache__/
  │   ├── database.cpython-313.pyc
  │   ├── main.cpython-313.pyc
  │   ├── models.cpython-313.pyc
  │   └── schemas.cpython-313.pyc
  ├── database.py
  ├── main.py
  ├── models.py
  ├── schemas.py
  └── tests/
      ├── init.py
      └── test_main.py
- enrollment.db
- frontend/
  ├── .gitignore
  ├── .vscode/
  │   └── extensions.json
  ├── README.md
  ├── index.html
  ├── package-lock.json
  ├── package.json
  ├── public/
  │   └── vite.svg
  ├── src/
  │   ├── App.vue
  │   ├── assets/
  │   │   └── vue.svg
  │   ├── components/
  │   │   └── HelloWorld.vue
  │   ├── main.js
  │   ├── style.css
  │   └── views/
  │       ├── CourseCreate.vue
  │       ├── Enroll.vue
  │       ├── StudentRegister.vue
  │       └── StudyTips.vue
  └── vite.config.js
- repos.code-workspace
- requirements.txt
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<YOUR_USERNAME>/course-enrollment-app.git
cd course-enrollment-app
```

### 2. Set up the backend

1. Create a virtual environment:

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

4. Run the backend:

```bash
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

> The database (`enrollment.db`) will be created automatically on first run.

### 3. Set up the frontend

1. Navigate to the frontend folder:

```bash
cd frontend
```

2. Install npm dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

- The frontend will run at `http://localhost:3000`  
- Axios calls will go to `http://localhost:8000`

### 4. Using Groq GenAI (Optional)

1. Make sure your `.env` has `GROQ_API_KEY`  
2. Use the `/genai/study-tips` endpoint. Example payload:

```json
{
  "course_title": "Mathematics 101",
  "credit_units": 3
}
```

The endpoint returns:

```json
{
  "tips": [
    "Practice daily problem-solving.",
    "Review lecture notes after each class.",
    "Use online tools for exercises."
  ]
}
```

### 5. Optional Tailwind CSS

If desired:

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Configure `tailwind.config.js` and include `@tailwind` in your CSS. Otherwise, plain CSS works perfectly.

---

## Running the Application

1. **Start backend** (`uvicorn api.main:app --reload`) → http://localhost:8000  
2. **Start frontend** (`npm run dev`) → http://localhost:3000  
3. Open in browser, test forms: register students, create courses, enroll, get study tips.

---

## Testing

Backend tests use **pytest**:

```bash
cd api/tests
pytest
```

Tests cover:  
- Creating students and courses  
- Enrolling students without duplicates  
- Listing student courses  
- Testing the GenAI endpoint with a mock response

---

## Using the App

- **Register a Student:** Fill in name and email  
- **Create a Course:** Enter title, code, credits, description  
- **Enroll:** Select student and course from dropdowns; duplicates are blocked  
- **Study Tips:** Select a course and get AI-generated tips (optional)

Everything works seamlessly together.

---

## Contributing

If you want to contribute:  
1. Fork the repository  
2. Create a branch: `git checkout -b feature/your-feature`  
3. Make your changes and commit: `git commit -m "Add feature"`  
4. Push to your branch: `git push origin feature/your-feature`  
5. Open a Pull Request

> **Note:** Never commit `.env` or sensitive files.

---

## License

This project is under the **MIT License** — see `LICENSE` file.

