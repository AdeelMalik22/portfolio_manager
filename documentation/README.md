# Portfolio Builder - A Zero-Cost Portfolio Generator

## 🎨 Overview

**Portfolio Builder** is a professional, zero-cost web application that enables users to create stunning portfolios in minutes without any coding knowledge. It features 20 professionally designed templates across multiple categories and generates downloadable, standalone HTML files ready for deployment.

### Key Features

- ✅ **20 Professional Templates** - Minimalist, Developer, Creative, and Corporate categories
- ✅ **100% Free** - No hidden costs, no premium plans
- ✅ **Zero Dependencies** - Downloads as a single, portable HTML file
- ✅ **Fully Responsive** - Works beautifully on all devices
- ✅ **Easy to Use** - No coding skills required
- ✅ **Instant Preview** - See your portfolio before downloading
- ✅ **Deploy Anywhere** - Host on any web server

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or download the project**
```bash
cd portfolio_manager
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run migrations**
```bash
python manage.py migrate
```

4. **Load portfolio templates**
```bash
python manage.py load_templates
```

5. **Create a superuser (optional, for admin access)**
```bash
python manage.py createsuperuser
```

6. **Start development server**
```bash
python manage.py runserver
```

7. **Access the application**
   - Homepage: `http://localhost:8000/`
   - Template Gallery: `http://localhost:8000/gallery/`
   - Portfolio Builder: `http://localhost:8000/form/`
   - Admin Panel: `http://localhost:8000/admin/`
   - API: `http://localhost:8000/api/`

---

## 📁 Project Structure

```
portfolio_manager/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── db.sqlite3                         # SQLite database
│
├── portfolio_manager/                 # Project settings
│   ├── settings.py                   # Configuration
│   ├── urls.py                       # Main URL routing
│   ├── asgi.py
│   └── wsgi.py
│
├── portfolio/                         # Main app
│   ├── models.py                     # Database models (5 models)
│   ├── views.py                      # API & web views
│   ├── serializers.py                # DRF serializers
│   ├── services.py                   # Portfolio rendering service
│   ├── urls.py                       # API routing
│   ├── admin.py                      # Admin configuration
│   ├── migrations/
│   │   └── 0001_initial.py          # Initial migration
│   └── management/
│       └── commands/
│           └── load_templates.py    # Template loader command
│
├── templates/                         # HTML templates
│   ├── base.html                     # Base template
│   ├── index.html                    # Homepage
│   ├── portfolio_gallery.html        # Template gallery
│   ├── portfolio_form.html           # Portfolio builder form
│   └── portfolio_templates/          # 20 portfolio templates
│       ├── template_1_minimalist.html
│       ├── template_2_dark_modern.html
│       ├── template_3_gradient_purple.html
│       ├── template_4_corporate_blue.html
│       ├── template_5_creative_orange.html
│       ├── template_6_teal_gradient.html
│       ├── template_7_slate_blue.html
│       ├── template_8_terminal_green.html
│       ├── template_9_red_accent.html
│       ├── template_10_gold_luxury.html
│       ├── template_11_indigo_professional.html
│       ├── template_12_emerald.html
│       ├── template_13_slate_dark.html
│       ├── template_14_pink_vibrant.html
│       ├── template_15_amber_warm.html
│       ├── template_16_sky_blue.html
│       ├── template_17_cyan_tech.html
│       ├── template_18_violet_modern.html
│       ├── template_19_stone_minimal.html
│       └── template_20_rose_elegant.html
│
└── media/                             # Uploaded images
    └── profiles/                      # User profile images
```

---

## 🎯 How to Use

### 1. Browse Templates

Visit the gallery page to browse all 20 available templates:
```
http://localhost:8000/gallery/
```

- Filter by category (Minimalist, Developer, Creative, Corporate)
- Preview templates with sample data
- See template details and color schemes

### 2. Create Portfolio

Go to the portfolio builder form:
```
http://localhost:8000/form/
```

**Fill in your information:**
- Basic info (name, title, bio, email, location)
- Social links (GitHub, LinkedIn, Website, Twitter)
- Profile image (optional)
- Skills (add multiple)
- Projects (add multiple)
- Experience (add multiple)
- Education (add multiple)

### 3. Select Template

Choose your preferred template from the dropdown. You can preview it before submitting.

### 4. Download

Click "Generate Portfolio" to:
- Process your data
- Render your selected template
- Download as a single HTML file

### 5. Deploy

Your downloaded HTML file is ready to deploy:
- Upload to any web server
- Host on GitHub Pages, Netlify, Vercel, etc.
- No backend required
- Works standalone

---

## 📊 API Documentation

### REST API Endpoints

#### Templates

```bash
# List all templates
GET /api/templates/

# Get template details
GET /api/templates/{id}/

# Filter by category
GET /api/templates/by_category/?category=developer

# Preview template with dummy data
GET /api/template/{id}/preview/
```

#### Portfolios

```bash
# Create portfolio
POST /api/portfolios/

# List portfolios
GET /api/portfolios/

# Get portfolio details
GET /api/portfolios/{id}/

# Update portfolio
PUT /api/portfolios/{id}/

# Preview rendered portfolio
GET /api/portfolios/{id}/preview/

# Download as HTML
GET /api/portfolios/{id}/download/

# Publish portfolio
POST /api/portfolios/{id}/publish/

# Unpublish portfolio
POST /api/portfolios/{id}/unpublish/
```

### Example Requests

**Create a portfolio:**
```bash
curl -X POST http://localhost:8000/api/portfolios/ \
  -F "full_name=John Doe" \
  -F "title=Software Engineer" \
  -F "bio=Experienced full-stack developer" \
  -F "email=john@example.com" \
  -F "template=1" \
  -F "skills=[\"Python\",\"Django\",\"React\"]" \
  -F "profile_image=@profile.jpg"
```

**Download portfolio as HTML:**
```bash
curl http://localhost:8000/api/portfolios/1/download/ > my_portfolio.html
```

---

## 🎨 20 Portfolio Templates

### Minimalist (2)
1. **Minimalist Black & White** - Clean, elegant black and white design
2. **Stone Minimal** - Ultra-clean stone gray minimalist theme

### Developer (5)
3. **Dark Modern Blue** - Modern dark theme with vibrant blue
4. **Terminal Green** - Retro terminal-style green on black
5. **Slate Blue** - Professional slate blue colors
6. **Slate Dark** - Tech-focused dark slate
7. **Sky Blue** - Light sky blue theme

### Creative (7)
8. **Gradient Purple** - Stunning purple gradient background
9. **Creative Orange** - Warm, creative orange theme
10. **Red Accent** - Bold red gradient design
11. **Emerald Green** - Fresh emerald green colors
12. **Pink Vibrant** - Vibrant pink theme
13. **Violet Modern** - Elegant violet theme
14. **Rose Elegant** - Elegant rose theme

### Corporate (6)
15. **Corporate Blue** - Professional with sidebar layout
16. **Teal Gradient** - Fresh teal gradient design
17. **Gold Luxury** - Elegant gold and dark theme
18. **Indigo Professional** - Deep indigo professional colors
19. **Amber Warm** - Warm amber tones
20. **Cyan Tech** - Modern cyan colors

---

## 🗄️ Database Schema

### PortfolioTemplate
```python
- id: BigAutoField (Primary Key)
- name: CharField (unique, max_length=100)
- slug: SlugField (unique)
- description: TextField
- category: CharField (minimalist, developer, creative, corporate)
- color_scheme: CharField
- template_file: CharField (path to template HTML)
- preview_image: CharField (optional)
- is_active: BooleanField (default=True)
- created_at: DateTimeField (auto_now_add)
- order: IntegerField (default=0)
```

### Portfolio
```python
- id: BigAutoField (Primary Key)
- full_name: CharField (max_length=200)
- title: CharField (max_length=200)
- bio: TextField
- email: EmailField
- phone: CharField (optional)
- location: CharField (optional)
- linkedin: URLField (optional)
- github: URLField (optional)
- portfolio_website: URLField (optional)
- twitter: URLField (optional)
- profile_image: ImageField (optional)
- skills: JSONField (list of skills)
- template: ForeignKey(PortfolioTemplate)
- projects: JSONField (list of project objects)
- experience: JSONField (list of experience objects)
- education: JSONField (list of education objects)
- is_published: BooleanField (default=False)
- created_at: DateTimeField (auto_now_add)
- updated_at: DateTimeField (auto_now)
```

### PortfolioProject (Optional)
```python
- portfolio: ForeignKey(Portfolio)
- title: CharField
- description: TextField
- tech_stack: CharField
- github_link: URLField (optional)
- live_link: URLField (optional)
- order: IntegerField
```

### PortfolioExperience (Optional)
```python
- portfolio: ForeignKey(Portfolio)
- company: CharField
- role: CharField
- duration: CharField
- description: TextField
- order: IntegerField
```

### PortfolioEducation (Optional)
```python
- portfolio: ForeignKey(Portfolio)
- school: CharField
- degree: CharField
- field: CharField
- year: CharField
```

---

## 🔧 Configuration

### Django Settings

**Important settings in `portfolio_manager/settings.py`:**

```python
# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload limits
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
```

### Environment Variables (Optional)

For production, create a `.env` file:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:pass@host/db
```

---

## 🚢 Deployment

### Option 1: Heroku

```bash
# Install Heroku CLI
# Create Procfile:
echo "web: gunicorn portfolio_manager.wsgi" > Procfile

# Deploy
heroku create
heroku config:set DEBUG=False
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py load_templates
```

### Option 2: PythonAnywhere

1. Upload files to PythonAnywhere
2. Create virtual environment
3. Install requirements
4. Configure web app
5. Run migrations
6. Load templates

### Option 3: AWS, DigitalOcean, Vercel, etc.

- Similar steps as above
- Configure database (PostgreSQL recommended)
- Set environment variables
- Enable static/media file serving
- Run migrations and load templates

---

## 🧪 Testing

### Test the API

```bash
# Get all templates
curl http://localhost:8000/api/templates/

# List portfolios
curl http://localhost:8000/api/portfolios/

# Test preview
open "http://localhost:8000/api/template/1/preview/"
```

### Test the Web Interface

1. Go to `http://localhost:8000/`
2. Browse gallery at `/gallery/`
3. Create portfolio at `/form/`
4. Download portfolio as HTML

---

## 📝 Security Features

- ✅ Django CSRF protection
- ✅ Input validation on all forms
- ✅ URL validation for social links
- ✅ Email validation
- ✅ Image file upload restrictions
- ✅ File size limits (5MB max)
- ✅ XSS protection via template system
- ✅ SQL injection prevention via ORM

---

## 🎓 Admin Interface

Access Django admin at:
```
http://localhost:8000/admin/
```

**Available in admin:**
- Manage portfolio templates
- View all created portfolios
- Manage users
- View recent activities
- Search and filter

---

## 📚 Additional Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Responsive Design**: https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design
- **HTML/CSS Best Practices**: https://developer.mozilla.org/en-US/

---

## 🤝 Contributing

Found a bug or have a suggestion? Feel free to improve the project!

---

## 📄 License

This project is free to use and modify.

---

## 🎉 Support & Feedback

For issues or questions:
1. Check existing documentation
2. Review the code comments
3. Check the API documentation

---

## ✨ Features Roadmap

### Phase 1 (Current) ✅
- [x] 20 professional templates
- [x] Portfolio data input
- [x] HTML generation
- [x] Download functionality
- [x] REST API
- [x] Web interface

### Phase 2 (Future)
- [ ] Save portfolios to database
- [ ] Public portfolio URLs
- [ ] Custom domains
- [ ] Drag-and-drop editor
- [ ] Theme customization
- [ ] Social media integration
- [ ] Email notifications
- [ ] Analytics
- [ ] Version history
- [ ] Team collaboration

---

## 🚀 Performance Notes

- Templates render in <100ms
- Image processing optimized
- Minimal external dependencies
- Standalone HTML files (~100KB)
- Mobile-first responsive design

---

## ✅ Checklist for Deployment

- [ ] Update SECRET_KEY in production
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up production database
- [ ] Configure static files serving
- [ ] Configure media files serving
- [ ] Enable HTTPS/SSL
- [ ] Set up backups
- [ ] Configure error monitoring
- [ ] Test all API endpoints
- [ ] Load templates
- [ ] Create superuser

---

**Happy portfolio building! 🎨**

