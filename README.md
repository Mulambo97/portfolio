# Personal Portfolio Website 🌐

[![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Deployment](https://img.shields.io/badge/deployed_on-Google_Cloud-4285F4?logo=google-cloud)](https://portfolio-lfr9.onrender.com)
[![Responsive Design](https://img.shields.io/badge/mobile-responsive-success)]()

## Purpose 🚀
A modern portfolio website to:
- Showcase professional experience and technical skills
- Display portfolio projects with interactive demos
- Provide professional contact information
- Demonstrate full-stack development capabilities

## Features ✨

### **Home Page** (`home.html`)
- Professional banner with responsive scaling
- Bio section with profile image and personal statement
- Skills showcase with technology icons
- Mobile-first responsive layout

### **Projects Page** (`projects.html`)
- Project cards with detailed descriptions
- Interactive elements with hover effects
- Direct links to live demos and GitHub repositories
- Responsive grid layout

### **Contact Page** (`resume.html`)
- Professional contact form with email integration
- Skills and project worked on

## Technologies Used 💻

**Frontend**
- HTML5 Semantic Markup
- CSS3 (Flexbox, Grid, Animations)
- JavaScript (ES6+)
- Responsive Design (Media Queries)

**DevOps**
- Docker Containerization
- Google Cloud Platform (Deployment)
- Git Version Control

## Local Development 🛠️

### Prerequisites
- Docker Desktop
- Modern web browser

### Setup Instructions
1. Clone repository:
```bash
git clone https://github.com/Mulambo97/portfolio.git
cd portfolio
```

2. Start development server:
```bash
docker-compose -f docker-compose.yml -p portfolio up
```

3. Access website at:
http://localhost:8080/home.html

4. Build and deploy to Google Cloud:
```bash 
gcloud builds submit --tag gcr.io/portfolio-1/portfolio
gcloud run deploy --image gcr.io/portfolio-1/portfolio--platform managed```

