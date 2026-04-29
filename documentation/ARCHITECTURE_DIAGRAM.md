# System Architecture & Data Flow

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Dashboard Edit         API Client         JavaScript        │
│  (HTML Form)        (Mobile/Desktop)    (image-processor.js)│
│                                                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
           ┌───────────┴───────────┐
           │                       │
           ▼                       ▼
┌──────────────────────┐ ┌────────────────────┐
│   DJANGO VIEWS       │ │  REST API          │
│  & SERIALIZERS       │ │  ENDPOINTS         │
├──────────────────────┤ ├────────────────────┤
│ PortfolioViewSet     │ │ /api/portfolios/   │
│ portfolio_form()     │ │ /api/my-portfolio/ │
│ process_my_portfolio │ │ .../process-image/ │
│ _image()             │ │                    │
└──────────┬───────────┘ └────────┬───────────┘
           │                      │
           └──────────┬───────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │   FORM LAYER                │
        ├─────────────────────────────┤
        │ PublicPortfolioForm         │
        │ - auto_process_image option │
        │ - Custom save() method       │
        └──────────────┬──────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │   IMAGE PROCESSOR SERVICE           │
        ├─────────────────────────────────────┤
        │ ImageProcessor                      │
        │ - remove_background()               │
        │ - create_themed_background()        │
        │ - merge_image_with_background()    │
        │ - process_image()                   │
        │ - save_processed_image()            │
        └──────────────┬──────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
    ┌────────────┐           ┌──────────────┐
    │ rembg      │           │ PIL + NumPy  │
    │ (AI)       │           │ (Fallback)   │
    │ Optional   │           │ Built-in     │
    └────────────┘           └──────────────┘
        │                             │
        └──────────────┬──────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │   DATABASE LAYER             │
        ├──────────────────────────────┤
        │ Portfolio Model              │
        │ - profile_image              │
        │ - processed_profile_image    │
        │                              │
        │ PublicPortfolio Model        │
        │ - profile_image              │
        │ - processed_profile_image    │
        └──────────┬───────────────────┘
                   │
                   ▼
        ┌──────────────────────────────┐
        │   FILE STORAGE               │
        ├──────────────────────────────┤
        │ media/profiles/              │
        │ media/profiles_processed/    │
        │ media/portfolio_profiles/    │
        │ media/portfolio_profiles_... │
        └──────────────────────────────┘
```

## 🔄 Image Processing Flow

```
START
  │
  ├─► User uploads image
  │    (JPG, PNG, GIF, BMP, WebP)
  │
  ├─► System receives upload
  │    via PortfolioViewSet.process_image()
  │    or dashboard form
  │
  ├─► ImageProcessor.process_image() called
  │    │
  │    ├─► 1. BACKGROUND REMOVAL
  │    │    ├─ Try: rembg (AI-powered)
  │    │    │   ✓ Analyzes edges
  │    │    │   ✓ Detects foreground
  │    │    │   ✓ Removes background
  │    │    │
  │    │    └─ Fallback: Color-based
  │    │       ✓ Samples corner pixels
  │    │       ✓ Detects background color
  │    │       ✓ Removes with tolerance
  │    │
  │    ├─► 2. THEME SELECTION
  │    │    ├─ Get template slug
  │    │    │  (modern_corporate, etc.)
  │    │    │
  │    │    └─ Load theme colors
  │    │       ├─ primary: (R, G, B)
  │    │       ├─ secondary: (R, G, B)
  │    │       └─ accent: (R, G, B)
  │    │
  │    ├─► 3. BACKGROUND GENERATION
  │    │    ├─ Create 600x600px canvas
  │    │    │
  │    │    └─ Draw gradient
  │    │       ├─ Top: primary color
  │    │       ├─ Middle: interpolated
  │    │       └─ Bottom: secondary color
  │    │
  │    ├─► 4. IMAGE COMPOSITION
  │    │    ├─ Scale subject
  │    │    │  └─ Height = 70% of canvas
  │    │    │
  │    │    ├─ Position image
  │    │    │  ├─ Horizontal: centered
  │    │    │  └─ Vertical: center-30px
  │    │    │
  │    │    └─ Add accent border
  │    │       └─ 5px line at bottom
  │    │
  │    └─► 5. OPTIMIZATION
  │         ├─ Ensure 600x600px
  │         ├─ Convert to PNG
  │         └─ Compress for web
  │
  ├─► ContentFile created
  │    └─ filename: processed_profile_*.png
  │
  ├─► Save to portfolio
  │    └─ portfolio.processed_profile_image = file
  │        portfolio.save()
  │
  ├─► Return success response
  │    ├─ Message: "Image processed successfully"
  │    └─ URL: /media/profiles_processed/...
  │
  └─► END

```

## 📱 Dashboard Integration Flow

```
User Dashboard
     │
     ├─► Edit Portfolio
     │
     ├─► File Input
     │    └─ onChange listener
     │       ├─ Read file
     │       ├─ Show original preview
     │       └─ Show process button
     │
     ├─► Click "🎨 Process Image"
     │    │
     │    ├─ Get image file
     │    ├─ Get template slug
     │    ├─ Show loading spinner
     │    │
     │    ├─ POST to /api/my-portfolio/process-image/
     │    │   ├─ Authorization header
     │    │   ├─ CSRF token
     │    │   └─ FormData (image, template_slug)
     │    │
     │    ├─ Wait for response (5-10s)
     │    │
     │    ├─ On success:
     │    │   ├─ Show processed image URL
     │    │   ├─ Display side-by-side
     │    │   ├─ Show success alert
     │    │   └─ Enable save button
     │    │
     │    └─ On error:
     │        ├─ Show error message
     │        └─ Allow retry
     │
     └─► Save Portfolio
          └─ Processed image automatically used
```

## 🔌 API Request/Response Flow

```
REQUEST:
┌──────────────────────────────────────┐
│ POST /api/my-portfolio/process-image/ │
├──────────────────────────────────────┤
│ Headers:                              │
│ - Authorization: Bearer TOKEN         │
│ - X-CSRFToken: csrf_token            │
│ - Content-Type: multipart/form-data  │
│                                       │
│ Body:                                 │
│ - image: (binary file)               │
│ - template_slug: "modern_corporate"  │
└──────────────────────────────────────┘
                │
                ▼
        PROCESS ON SERVER
                │
                ▼
RESPONSE (200 OK):
┌──────────────────────────────────────┐
│ {                                     │
│   "message": "Image processed...",   │
│   "portfolio": {                      │
│     "id": 1,                          │
│     "full_name": "John Doe",         │
│     "title": "Developer",             │
│     "profile_image": "...",          │
│     "processed_profile_image":        │
│       "https://...png",              │
│     ...                              │
│   }                                   │
│ }                                     │
└──────────────────────────────────────┘

OR ERROR (400 Bad Request):
┌──────────────────────────────────────┐
│ {                                     │
│   "error": "Image processing failed: │
│            (error details)"           │
│ }                                     │
└──────────────────────────────────────┘
```

## 📊 Data Model Relationships

```
┌─────────────────────────────────────┐
│        Portfolio Model              │
├─────────────────────────────────────┤
│ - id                                │
│ - full_name                         │
│ - title                             │
│ - bio                               │
│ - profile_image (original)          │
│ ★ processed_profile_image (NEW!)    │◄─┐
│ - template (FK)                     │  │
│ - created_at                        │  │
│ - updated_at                        │  │
└─────────────────────────────────────┘  │
                                         │
                                    References
                                         │
                                         │
┌─────────────────────────────────────┐  │
│     PublicPortfolio Model           │  │
├─────────────────────────────────────┤  │
│ - id                                │  │
│ - user (FK)                         │  │
│ - full_name                         │  │
│ - title                             │  │
│ - bio                               │  │
│ - profile_image (original)          │  │
│ ★ processed_profile_image (NEW!)    │◄─┤
│ - template (FK)                     │  │
│ - is_published                      │  │
│ - created_at                        │  │
│ - updated_at                        │  │
└─────────────────────────────────────┘  │
                                         │
                                    References
                                         │
                                    ┌────┴──────────────┐
                                    │                   │
                          ┌─────────▼──────────┐   ┌────▼────────┐
                          │ PortfolioTemplate  │   │ Media Files  │
                          ├───────────────────┤   ├──────────────┤
                          │ - id              │   │ profiles/    │
                          │ - name            │   │ profiles_... │
                          │ - slug            │   │ portfolio_.. │
                          │ - colors          │   │ portfolio_..│
                          │ - template_file   │   │              │
                          └───────────────────┘   └──────────────┘
```

## 🌊 Theme Color Application

```
Template: Modern Corporate

Colors:
┌─────────────────────────────────┐
│ Primary:   #1a202e              │ (Top)
│ Secondary: #2d3748              │ (Bottom)
│ Accent:    #ff9900              │ (Border)
└─────────────────────────────────┘

Applied to Background:
┌──────────────────────────────┐
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░  │ ← Primary (#1a202e)
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░  │ 
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    │ ← Gradient interpolation
│ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    │
│ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    │ ← Secondary (#2d3748)
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    │
│ ███████████████████████████ │ ← Accent (#ff9900) border
└──────────────────────────────┘
```

## 🎨 Image Composition

```
Original Image:             Theme Background:      Final Output:
┌─────────────────┐        ┌──────────────────┐   ┌──────────────────┐
│                 │        │░░░░░░░░░░░░░░░░░░│   │░░░░░░░░░░░░░░░░░░│
│                 │        │░░░░░░░░░░░░░░░░░░│   │░░░░░░░░░░░░░░░░░░│
│    ╔════════╗   │        │░░░░░░░░░░░░░░░░░░│   │░░░  ╔════════╗  ░░│
│    ║  FACE  ║   │        │░░░░░░░░░░░░░░░░░░│   │░░░  ║  FACE  ║  ░░│
│    ║ WITHOUT║───+──────→ │░░░░░░░░░░░░░░░░░░│ + │░░░  ║ MERGED║  ░░│
│    ║  BG    ║   │        │░░░░░░░░░░░░░░░░░░│   │░░░  ║WITH BG║  ░░│
│    ╚════════╝   │        │░░░░░░░░░░░░░░░░░░│   │░░░  ╚════════╝  ░░│
│                 │        │░░░░░░░░░░░░░░░░░░│   │░░░░░░░░░░░░░░░░░░│
└─────────────────┘        │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│   │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
                           │███████████████████│   │███████████████████│
600x600 RGBA               └──────────────────┘   └──────────────────┘
Transparent BG             600x600 RGB            600x600 PNG
                           Gradient               Final Output
```

## 📋 Processing States

```
State Machine:

[IDLE]
  ├─ User selects image
  │  └─ [PREVIEW]
  │     ├─ Show original image
  │     └─ Enable process button
  │
  ├─ User clicks process
  │  └─ [PROCESSING]
  │     ├─ Show spinner
  │     ├─ Send to server
  │     └─ Wait for response (5-10s)
  │
  ├─ Success
  │  └─ [SUCCESS]
  │     ├─ Show processed image
  │     ├─ Display alert
  │     └─ Enable save
  │
  └─ Error
     └─ [ERROR]
        ├─ Show error message
        └─ Allow retry
```

## 🔐 Security Flow

```
Request Validation:
  1. Authentication check
     └─ Bearer token valid?
  
  2. File type validation
     └─ image/* MIME type?
  
  3. File size validation
     └─ < 50MB?
  
  4. CSRF token validation
     └─ Token present & valid?
  
  5. User ownership check
     └─ User owns portfolio?

  ✓ All passed → Process image
  ✗ Any failed → Return 400/401/403
```

## 📈 Performance Metrics

```
Processing Speed:

Small Image (<500KB):
  1. Remove background: 1s
  2. Create background: 0.5s
  3. Compose image: 0.5s
  ────────────────────
  Total: ~2-3 seconds

Medium Image (500KB-2MB):
  1. Remove background: 3s
  2. Create background: 0.5s
  3. Compose image: 1s
  ────────────────────
  Total: ~3-5 seconds

Large Image (>2MB):
  1. Remove background: 5-8s
  2. Create background: 0.5s
  3. Compose image: 1s
  ────────────────────
  Total: ~5-10 seconds

Output Size:
  Original: Varies
  Processed: 50-200 KB (PNG, 600x600)
  Savings: Optimized for web
```

---

**Diagram Version**: 1.0  
**Date**: April 29, 2026

