# EduWrite - Educational Writing Analysis Tool

An educational platform designed for universities to help students understand writing patterns, detect AI-generated content, and improve their writing skills through interactive exercises.

## Features

### 1. Plagiarism Detection
- TF-IDF based similarity checking
- Common phrase detection
- Internal repetition analysis

### 2. AI Content Detection
- Statistical analysis of writing patterns
- Sentence uniformity measurement
- Burstiness calculation (complexity variation)
- Vocabulary richness analysis
- Transition word density tracking

### 3. Sentence-by-Sentence Breakdown
- Individual analysis of each sentence
- Color-coded indicators (AI-like vs Human)
- Specific fix suggestions for each issue
- Identifies:
  - Formal transitions
  - Filler phrases
  - Passive voice
  - Uniform sentence length
  - Personal pronouns
  - Contractions
  - Conversational tone

### 4. Interactive Writing Exercises
Personalized exercises based on submitted text:

| Exercise | Difficulty | Learning Goal |
|----------|------------|---------------|
| Add Your Personal Voice | Easy | Using personal perspective |
| Create Rhythm with Variety | Medium | Varying sentence lengths |
| Cut the Fluff | Easy | Removing filler phrases |
| Make It Active | Medium | Converting passive to active voice |
| Engage with Questions | Easy | Adding rhetorical questions |
| Show Both Sides | Hard | Adding nuance and contrast |

### 5. Humanization Suggestions
- Side-by-side comparison (original vs improved)
- Detailed explanation of each change
- Educational focus on WHY changes improve writing

### 6. User Features
- User authentication (register/login)
- Document history tracking
- Learning progress dashboard
- Learning center with tips and exercises

## Tech Stack

- **Backend:** Django 4.2
- **Frontend:** Bootstrap 5, Font Awesome
- **AI/ML:** scikit-learn, NumPy
- **Database:** SQLite (development), PostgreSQL (production ready)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/iamkumarji/plagiarism-website-.git
   cd plagiarism-website-
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## Project Structure

```
plagiarism-website-/
├── analyzer/                   # Main application
│   ├── models.py              # Database models
│   ├── views.py               # View logic
│   ├── urls.py                # URL routing
│   └── services/              # Core analysis modules
│       ├── plagiarism_detector.py
│       ├── ai_detector.py
│       └── humanizer.py
├── eduwrite/                   # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/analyzer/         # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── dashboard.html
│   ├── analyze.html
│   ├── result.html
│   ├── history.html
│   ├── learning.html
│   ├── login.html
│   └── register.html
├── static/                     # Static files (CSS, JS)
├── manage.py
├── requirements.txt
└── README.md
```

## Usage

### For Students

1. **Register/Login** - Create an account to track your progress
2. **Analyze Text** - Paste your essay or assignment
3. **Review Results** - See plagiarism score, AI detection score, and detailed breakdown
4. **Learn from Breakdown** - Understand why each sentence is flagged
5. **Practice Exercises** - Complete interactive exercises based on your text
6. **Track Progress** - Monitor improvement over time in the dashboard

### For Universities

- Deploy on private network/computer labs
- Students can only access within controlled environment
- Institutional oversight maintained
- Focus on education, not evasion

## Configuration

### Environment Variables (for production)

Create a `.env` file:
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgres://user:pass@localhost/dbname
```

### Database (Production)

For PostgreSQL:
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'eduwrite',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/register/` | GET, POST | User registration |
| `/login/` | GET, POST | User login |
| `/logout/` | GET | User logout |
| `/dashboard/` | GET | User dashboard |
| `/analyze/` | GET, POST | Text analysis page |
| `/result/<id>/` | GET | Analysis results |
| `/history/` | GET | Document history |
| `/learning/` | GET | Learning center |
| `/api/quick-analyze/` | POST | Quick analysis API (JSON) |

## How Detection Works

### AI Detection Algorithm

The AI detector analyzes text using multiple statistical features:

1. **Sentence Uniformity** - AI tends to produce sentences of similar length
2. **Burstiness** - Human writing has more variation in complexity
3. **Vocabulary Richness** - Type-Token Ratio analysis
4. **Transition Density** - AI overuses formal transitions
5. **Filler Phrase Detection** - Identifies AI padding phrases

### Scoring

- **0-30%**: Likely human-written
- **30-60%**: Mixed characteristics
- **60-100%**: Strong AI indicators

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is for educational purposes. Please use responsibly.

## Acknowledgments

- Built with Django
- UI powered by Bootstrap 5
- Icons by Font Awesome
- ML algorithms from scikit-learn

---

**Note:** This tool is designed for educational purposes to help students understand writing patterns and improve their skills. It is NOT intended to help bypass detection systems.
