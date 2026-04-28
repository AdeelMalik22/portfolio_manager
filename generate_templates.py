#!/usr/bin/env python
"""
Generate 20 professional, enterprise-grade portfolio templates
Based on comprehensive design specifications
"""

import os
import json

# Template specifications
TEMPLATES = {
    # MINIMALIST (4)
    "template_1_minimalist_dark_elegance": {
        "name": "Minimalist Dark Elegance",
        "category": "minimalist",
        "color_scheme": "navy-red",
        "description": "Dark background with white text and red accent. Extreme simplicity, typography-first design.",
        "colors": {
            "primary": "#1a1a2e",
            "secondary": "#0f3460",
            "accent": "#e94560",
            "text": "#ffffff",
            "background": "#16213e",
            "neutral": "#e0e0e0"
        }
    },
    "template_2_minimalist_light_clean": {
        "name": "Minimalist Light Clean",
        "category": "minimalist",
        "color_scheme": "light-blue",
        "description": "White background with minimal colors. Maximum readability and clarity.",
        "colors": {
            "primary": "#006994",
            "secondary": "#004d6d",
            "accent": "#00d4ff",
            "text": "#1a1a1a",
            "background": "#ffffff",
            "neutral": "#f5f5f5"
        }
    },
    "template_3_minimalist_monochrome": {
        "name": "Minimalist Monochrome",
        "category": "minimalist",
        "color_scheme": "black-white",
        "description": "Pure black & white. Ultimate simplicity, print-ready design.",
        "colors": {
            "primary": "#000000",
            "secondary": "#333333",
            "accent": "#666666",
            "text": "#000000",
            "background": "#ffffff",
            "neutral": "#cccccc"
        }
    },
    "template_4_minimalist_serif_classic": {
        "name": "Minimalist Serif Classic",
        "category": "minimalist",
        "color_scheme": "cream-gold",
        "description": "Serif typography focused design. Timeless, editorial aesthetic.",
        "colors": {
            "primary": "#3d3d3d",
            "secondary": "#5a5a5a",
            "accent": "#d4af37",
            "text": "#2a2a2a",
            "background": "#f5f1e8",
            "neutral": "#e8e4da"
        }
    },
    # DEVELOPER (6)
    "template_5_developer_dark_tech": {
        "name": "Developer Dark Tech",
        "category": "developer",
        "color_scheme": "terminal-green",
        "description": "Terminal-inspired dark theme. Perfect for software engineers.",
        "colors": {
            "primary": "#0a0a0a",
            "secondary": "#1a1a1a",
            "accent": "#00ff41",
            "text": "#00ff41",
            "background": "#0f0f0f",
            "neutral": "#333333"
        }
    },
    "template_6_developer_modern_blue": {
        "name": "Developer Modern Blue",
        "category": "developer",
        "color_scheme": "blue-purple",
        "description": "Modern gradient with glassmorphism cards. Blue to purple transition.",
        "colors": {
            "primary": "#667eea",
            "secondary": "#764ba2",
            "accent": "#f093fb",
            "text": "#ffffff",
            "background": "#0a1428",
            "neutral": "#1f2937"
        }
    },
    "template_7_developer_neon_cyberpunk": {
        "name": "Developer Neon Cyberpunk",
        "category": "developer",
        "color_scheme": "neon-cyber",
        "description": "Cyberpunk aesthetic with neon colors and glowing effects.",
        "colors": {
            "primary": "#0a0e27",
            "secondary": "#1a1a3e",
            "accent": "#f093fb",
            "text": "#00d4ff",
            "background": "#0d0221",
            "neutral": "#ff006e"
        }
    },
    "template_8_developer_corporate_tech": {
        "name": "Developer Corporate Tech",
        "category": "developer",
        "color_scheme": "corporate-cyan",
        "description": "Professional tech company aesthetic. Data-focused design.",
        "colors": {
            "primary": "#004d6d",
            "secondary": "#003d52",
            "accent": "#00d4ff",
            "text": "#ffffff",
            "background": "#0a1929",
            "neutral": "#1a3a4a"
        }
    },
    "template_9_developer_gradient_sunset": {
        "name": "Developer Gradient Sunset",
        "category": "developer",
        "color_scheme": "sunset",
        "description": "Warm gradients with sunset colors. Modern creative feel.",
        "colors": {
            "primary": "#ff6b35",
            "secondary": "#f7931e",
            "accent": "#c42e3b",
            "text": "#ffffff",
            "background": "#1a1423",
            "neutral": "#3d3d3d"
        }
    },
    "template_10_developer_glassmorphism": {
        "name": "Developer Glassmorphism",
        "category": "developer",
        "color_scheme": "glass-dark",
        "description": "Frosted glass effect cards. Modern depth and transparency.",
        "colors": {
            "primary": "#667eea",
            "secondary": "#764ba2",
            "accent": "#f093fb",
            "text": "#ffffff",
            "background": "#1a1a2e",
            "neutral": "rgba(255, 255, 255, 0.1)"
        }
    },
    # CREATIVE (6)
    "template_11_creative_forest_green": {
        "name": "Creative Forest Green",
        "category": "creative",
        "color_scheme": "forest",
        "description": "Natural, organic feel with forest green colors.",
        "colors": {
            "primary": "#1b4332",
            "secondary": "#2d6a4f",
            "accent": "#52b788",
            "text": "#1a1a1a",
            "background": "#f1faee",
            "neutral": "#e8f5e9"
        }
    },
    "template_12_creative_vibrant_rainbow": {
        "name": "Creative Vibrant Rainbow",
        "category": "creative",
        "color_scheme": "rainbow",
        "description": "Colorful, energetic, and bold. Dynamic layouts.",
        "colors": {
            "primary": "#ff006e",
            "secondary": "#00d4ff",
            "accent": "#ffbe0b",
            "text": "#1a1a1a",
            "background": "#ffffff",
            "neutral": "#f5f5f5"
        }
    },
    "template_13_creative_pastel_dream": {
        "name": "Creative Pastel Dream",
        "category": "creative",
        "color_scheme": "pastel",
        "description": "Soft pastels. Dreamy, gentle aesthetic.",
        "colors": {
            "primary": "#c9b1ff",
            "secondary": "#b4a7ff",
            "accent": "#ff8fa3",
            "text": "#4a4a4a",
            "background": "#fffef8",
            "neutral": "#f5f3ff"
        }
    },
    "template_14_creative_bold_typography": {
        "name": "Creative Bold Typography",
        "category": "creative",
        "color_scheme": "bold-type",
        "description": "Large, artistic typography. Design-driven layout.",
        "colors": {
            "primary": "#ff006e",
            "secondary": "#fb5607",
            "accent": "#ffbe0b",
            "text": "#1a1a1a",
            "background": "#ffffff",
            "neutral": "#f0f0f0"
        }
    },
    "template_15_creative_3d_modern": {
        "name": "Creative 3D Modern",
        "category": "creative",
        "color_scheme": "3d-depth",
        "description": "3D effects and perspective transforms. Modern depth.",
        "colors": {
            "primary": "#667eea",
            "secondary": "#764ba2",
            "accent": "#f093fb",
            "text": "#ffffff",
            "background": "#0a1428",
            "neutral": "#2a3a4a"
        }
    },
    "template_16_creative_retro_vintage": {
        "name": "Creative Retro Vintage",
        "category": "creative",
        "color_scheme": "vintage",
        "description": "Retro 80s/90s aesthetic. Nostalgic feel.",
        "colors": {
            "primary": "#e74c3c",
            "secondary": "#f39c12",
            "accent": "#9b59b6",
            "text": "#2c3e50",
            "background": "#ecf0f1",
            "neutral": "#bdc3c7"
        }
    },
    # CORPORATE (4)
    "template_17_corporate_executive_blue": {
        "name": "Corporate Executive Blue",
        "category": "corporate",
        "color_scheme": "executive",
        "description": "Traditional corporate. Trustworthy and professional.",
        "colors": {
            "primary": "#1a1a2e",
            "secondary": "#0f3460",
            "accent": "#d4af37",
            "text": "#ffffff",
            "background": "#16213e",
            "neutral": "#e0e0e0"
        }
    },
    "template_18_corporate_modern_gradient": {
        "name": "Corporate Modern Gradient",
        "category": "corporate",
        "color_scheme": "corp-gradient",
        "description": "Corporate with modern gradient touch.",
        "colors": {
            "primary": "#0066cc",
            "secondary": "#0052a3",
            "accent": "#00d4ff",
            "text": "#ffffff",
            "background": "#f5f7fa",
            "neutral": "#e1e8f0"
        }
    },
    "template_19_corporate_minimal_business": {
        "name": "Corporate Minimal Business",
        "category": "corporate",
        "color_scheme": "minimal-corp",
        "description": "Strict corporate minimal. Professional and serious.",
        "colors": {
            "primary": "#2c3e50",
            "secondary": "#34495e",
            "accent": "#3498db",
            "text": "#2c3e50",
            "background": "#ecf0f1",
            "neutral": "#bdc3c7"
        }
    },
    "template_20_corporate_modern_serif": {
        "name": "Corporate Modern Serif",
        "category": "corporate",
        "color_scheme": "serif-luxury",
        "description": "Elegant serif typography with luxury feel.",
        "colors": {
            "primary": "#1a3a52",
            "secondary": "#2d5a7a",
            "accent": "#d4af37",
            "text": "#1a1a1a",
            "background": "#f5f1e8",
            "neutral": "#e8e4da"
        }
    },
}

def generate_template_html(template_name, template_data):
    """Generate professional HTML template"""
    colors = template_data['colors']

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{ full_name }}}} - Portfolio</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --primary: {colors['primary']};
            --secondary: {colors['secondary']};
            --accent: {colors['accent']};
            --text: {colors['text']};
            --background: {colors['background']};
            --neutral: {colors['neutral']};
            --spacing-unit: 8px;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background-color: var(--background);
            color: var(--text);
            line-height: 1.6;
            overflow-x: hidden;
        }}

        /* HERO SECTION */
        .hero {{
            min-height: 100vh;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 60px 20px;
            position: relative;
            overflow: hidden;
        }}

        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255,255,255,0.05)" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,122.7C672,117,768,139,864,144C960,149,1056,139,1152,128C1248,117,1344,107,1392,101.3L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>') repeat;
            opacity: 0.5;
        }}

        .hero-content {{
            position: relative;
            z-index: 1;
            max-width: 800px;
            animation: fadeInUp 1s ease-out;
        }}

        .profile-img {{
            width: 200px;
            height: 200px;
            border-radius: 50%;
            margin: 0 auto 40px;
            border: 5px solid rgba(255, 255, 255, 0.2);
            object-fit: cover;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            animation: slideDown 0.8s ease-out;
        }}

        .hero h1 {{
            font-size: clamp(2.5rem, 8vw, 4rem);
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 15px;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }}

        .hero .title {{
            font-size: clamp(1.2rem, 4vw, 1.8rem);
            font-weight: 500;
            opacity: 0.95;
            margin-bottom: 20px;
            letter-spacing: 0.5px;
        }}

        .hero p {{
            font-size: 1.1rem;
            line-height: 1.8;
            max-width: 500px;
            margin: 0 auto 40px;
            opacity: 0.9;
        }}

        .cta-button {{
            display: inline-block;
            background-color: var(--accent);
            color: var(--text);
            padding: 15px 40px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            border: none;
            cursor: pointer;
        }}

        .cta-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        }}

        /* MAIN CONTAINER */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 80px 40px;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 40px 20px;
            }}
        }}

        /* SECTION STYLES */
        section {{
            margin-bottom: 80px;
        }}

        section h2 {{
            font-size: clamp(2rem, 5vw, 2.8rem);
            font-weight: 700;
            margin-bottom: 50px;
            color: var(--primary);
            position: relative;
            padding-bottom: 15px;
        }}

        section h2::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 60px;
            height: 4px;
            background: linear-gradient(90deg, var(--accent), var(--primary));
            border-radius: 2px;
        }}

        /* SKILLS */
        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 20px;
        }}

        .skill-badge {{
            background: rgba(var(--primary-rgb), 0.1);
            border: 2px solid var(--primary);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .skill-badge:hover {{
            transform: scale(1.05);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            background: var(--accent);
            color: var(--background);
        }}

        .skill-badge i {{
            font-size: 2rem;
            margin-bottom: 10px;
            display: block;
            color: var(--accent);
        }}

        .skill-badge:hover i {{
            color: var(--background);
        }}

        /* PROJECTS */
        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }}

        .project-card {{
            background: var(--primary);
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }}

        .project-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
        }}

        .project-image {{
            width: 100%;
            height: 200px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 3rem;
        }}

        .project-content {{
            padding: 25px;
            background: var(--background);
            color: var(--text);
        }}

        .project-content h3 {{
            color: var(--primary);
            font-size: 1.3rem;
            margin-bottom: 10px;
        }}

        .project-content p {{
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 15px;
            opacity: 0.8;
        }}

        .tech-stack {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }}

        .tech-tag {{
            background: var(--accent);
            color: var(--background);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }}

        .project-links {{
            display: flex;
            gap: 10px;
        }}

        .project-links a {{
            flex: 1;
            padding: 10px;
            background: var(--accent);
            color: var(--background);
            text-align: center;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }}

        .project-links a:hover {{
            opacity: 0.8;
        }}

        /* CONTACT */
        .contact-section {{
            text-align: center;
            padding: 60px 40px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 12px;
            color: white;
        }}

        .contact-section h2 {{
            color: white;
        }}

        .contact-links {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 30px 0;
            flex-wrap: wrap;
        }}

        .contact-link {{
            display: flex;
            flex-direction: column;
            align-items: center;
            text-decoration: none;
            color: white;
            transition: all 0.3s ease;
        }}

        .contact-link:hover {{
            transform: scale(1.1);
        }}

        .contact-link i {{
            font-size: 2rem;
            margin-bottom: 10px;
        }}

        /* FOOTER */
        footer {{
            background: rgba(0, 0, 0, 0.1);
            padding: 40px 20px;
            text-align: center;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--neutral);
        }}

        /* ANIMATIONS */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes slideDown {{
            from {{
                opacity: 0;
                transform: translateY(-20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes fadeIn {{
            from {{
                opacity: 0;
            }}
            to {{
                opacity: 1;
            }}
        }}

        /* RESPONSIVE */
        @media (max-width: 768px) {{
            .projects-grid {{
                grid-template-columns: 1fr;
            }}

            .skills-grid {{
                grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            }}

            .contact-links {{
                gap: 20px;
            }}

            .hero {{
                padding: 40px 20px;
            }}
        }}
    </style>
</head>
<body>
    <!-- HERO SECTION -->
    <section class="hero">
        <div class="hero-content">
            {{% if profile_image_base64 %}}
                <img src="{{{{ profile_image_base64 }}}}" alt="{{{{ full_name }}}}" class="profile-img">
            {{% else %}}
                <div class="profile-img" style="background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center;">
                    <i class="fas fa-user" style="font-size: 4rem; color: white;"></i>
                </div>
            {{% endif %}}
            <h1>{{{{ full_name }}}}</h1>
            <p class="title">{{{{ title }}}}</p>
            <p>{{{{ bio }}}}</p>
            <a href="mailto:{{{{ email }}}}" class="cta-button">Get In Touch</a>
        </div>
    </section>

    <div class="container">
        <!-- SKILLS -->
        {{% if skills %}}
        <section>
            <h2>Skills</h2>
            <div class="skills-grid">
                {{% for skill in skills %}}
                <div class="skill-badge">
                    <i class="fas fa-code"></i>
                    {{{{ skill }}}}
                </div>
                {{% endfor %}}
            </div>
        </section>
        {{% endif %}}

        <!-- PROJECTS -->
        {{% if projects %}}
        <section>
            <h2>Featured Projects</h2>
            <div class="projects-grid">
                {{% for project in projects %}}
                <div class="project-card">
                    <div class="project-image">
                        <i class="fas fa-laptop-code"></i>
                    </div>
                    <div class="project-content">
                        <h3>{{{{ project.title }}}}</h3>
                        <p>{{{{ project.description }}}}</p>
                        {{% if project.tech_stack %}}
                        <div class="tech-stack">
                            {{% for tech in project.tech_stack.split(',') %}}
                            <span class="tech-tag">{{{{ tech|trim }}}}</span>
                            {{% endfor %}}
                        </div>
                        {{% endif %}}
                        {{% if project.github_link or project.live_link %}}
                        <div class="project-links">
                            {{% if project.github_link %}}
                            <a href="{{{{ project.github_link }}}}" target="_blank">GitHub</a>
                            {{% endif %}}
                            {{% if project.live_link %}}
                            <a href="{{{{ project.live_link }}}}" target="_blank">Live Demo</a>
                            {{% endif %}}
                        </div>
                        {{% endif %}}
                    </div>
                </div>
                {{% endfor %}}
            </div>
        </section>
        {{% endif %}}

        <!-- CONTACT -->
        <section class="contact-section">
            <h2>Let's Connect</h2>
            <div class="contact-links">
                <a href="mailto:{{{{ email }}}}" class="contact-link">
                    <i class="fas fa-envelope"></i>
                    <span>Email</span>
                </a>
                {{% if github %}}
                <a href="{{{{ github }}}}" target="_blank" class="contact-link">
                    <i class="fab fa-github"></i>
                    <span>GitHub</span>
                </a>
                {{% endif %}}
                {{% if linkedin %}}
                <a href="{{{{ linkedin }}}}" target="_blank" class="contact-link">
                    <i class="fab fa-linkedin"></i>
                    <span>LinkedIn</span>
                </a>
                {{% endif %}}
                {{% if twitter %}}
                <a href="{{{{ twitter }}}}" target="_blank" class="contact-link">
                    <i class="fab fa-twitter"></i>
                    <span>Twitter</span>
                </a>
                {{% endif %}}
            </div>
        </section>
    </div>

    <!-- FOOTER -->
    <footer>
        <p>&copy; 2026 {{{{ full_name }}}}. All rights reserved.</p>
    </footer>

    <script>
        // Intersection Observer for animations
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        }};

        const observer = new IntersectionObserver(function(entries) {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
                    observer.unobserve(entry.target);
                }}
            }});
        }}, observerOptions);

        document.querySelectorAll('section').forEach(section => {{
            observer.observe(section);
        }});

        // Smooth scroll
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth' }});
                }}
            }});
        }});
    </script>
</body>
</html>
'''
    return html

# Main execution
if __name__ == "__main__":
    template_dir = "templates/portfolio_templates"
    os.makedirs(template_dir, exist_ok=True)

    print("\n🎨 Generating 20 Professional Enterprise Templates...\n")

    for template_key, template_data in TEMPLATES.items():
        html = generate_template_html(template_key, template_data)
        filepath = f"{template_dir}/{template_key}.html"

        with open(filepath, 'w') as f:
            f.write(html)

        print(f"✅ {template_data['name']}")

    print(f"\n🎉 Successfully created all 20 professional templates!")
    print(f"📁 Location: {template_dir}/")

