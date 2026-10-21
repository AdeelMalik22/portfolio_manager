# PortfolioForge Architecture Report

## Audit scope and basis

This report is a read-only audit of the current repository state on `master` at
commit `16270f0` (`chore(deploy): define Railway web start command`). The audit
was performed against the source tree, Django configuration, local database
catalogue, tests, and template files.

Current verified state:

- 34 active portfolio templates are registered in the local database.
- Active categories are `minimalist` (3), `developer` (11), `creative` (12),
  and `corporate` (8). The `latest` choice exists but currently has no active
  records.
- Every active template record points to an existing HTML template file.
- The portfolio test suite passes: 26 tests, 0 failures.
- The existing untracked `ideas/` directory was not inspected or changed.

No application functionality or portfolio template was changed for this audit.
The only intended repository addition is this report.

## 1. Technology stack

### Application

- Python/Django server-rendered web application.
- Django 5.2.13.
- Django REST Framework 3.17.1 for JSON APIs.
- SimpleJWT 5.5.1 for JWT authentication.
- Pillow 12.2.0 for image handling.
- `rembg`, NumPy, OpenCV, scikit-image, and ONNX Runtime for optional
  background removal and image processing.
- Gunicorn for deployment; `Procfile` starts `portfolio_manager.wsgi` on
  Railway-style `$PORT`.
- WhiteNoise serves compressed, manifest-based static files.
- Configured deployment runtime: Python 3.11 (`runtime.txt`). The current local
  virtual environment reports Python 3.10.12, so local and deployment Python
  versions should be aligned before the premium-template phase.

### Persistence and configuration

- SQLite fallback through `db.sqlite3`.
- `dj-database-url` allows a deployment database URL, such as PostgreSQL, to
  replace the SQLite default.
- User-uploaded media is stored below `media/` through Django `ImageField`s.
- Templates are loaded from the project-level `templates/` directory with
  Django app template discovery also enabled.

### Frontend

- Django templates with inline HTML and CSS.
- No frontend framework or bundler is present.
- Small amounts of inline JavaScript power builder/gallery interactions.
- The only extracted JavaScript asset is
  `portfolio/static/js/image-processor.js`.
- Most portfolio template styling is embedded in each template file. Google
  Fonts are linked from individual templates or the shared base template.

## 2. Relevant directory tree

```text
portfolio_manager/
├── manage.py
├── Procfile
├── runtime.txt
├── requirements.txt
├── db.sqlite3
├── portfolio_manager/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── portfolio/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   ├── forms.py
│   ├── services.py
│   ├── preview_context.py
│   ├── image_processor.py
│   ├── admin.py
│   ├── templatetags/portfolio_extras.py
│   ├── static/js/image-processor.js
│   ├── management/commands/
│   │   ├── load_templates.py
│   │   ├── load_templates_professional.py
│   │   └── generate_template_preview_pack.py
│   ├── migrations/
│   └── tests/test_previews.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── portfolio_gallery.html
│   ├── portfolio_form.html
│   ├── portfolio_edit.html
│   ├── dashboard.html
│   └── portfolio_templates/
│       ├── _portfolio_base.html
│       └── template_*.html
├── media/
│   └── profiles/
└── scripts/
    ├── generate_templates.py
    ├── generate_modern_templates.py
    └── image_processor_smoke.py
```

The `ideas/` directory is present as an untracked user directory and was left
outside this audit's working set.

## 3. Template architecture

### Template records and registry

`portfolio/models.py` defines `PortfolioTemplate` with these catalog fields:

- `name` and `slug` — unique identity.
- `description` — gallery/API description.
- `category` — currently limited to minimalist, developer, creative, corporate,
  and latest choices.
- `color_scheme` — a descriptive string used in the renderer context and image
  theme lookup.
- `template_file` — Django template path, for example
  `portfolio_templates/template_case_study_magazine.html`.
- `preview_image` — optional legacy string field; it is exposed by the API but
  is not currently used by the gallery.
- `is_active` and `order` — publication and display ordering.

The maintained catalogue is manually defined in
`portfolio/management/commands/load_templates.py`. The command updates existing
records by slug, creates missing records, reactivates maintained records, and
deactivates known deprecated slugs. The compatibility command
`load_templates_professional.py` delegates to this maintained command.

The database currently contains the authoritative runtime set. The source
registry and the tracked `db.sqlite3` therefore need to remain synchronized.
Running the management command is part of adding or changing catalog records;
it is not automatically invoked by the web process.

### Current template families

There are 34 active templates plus the shared partial:

- 12 active templates inherit from `portfolio_templates/_portfolio_base.html`:
  `base_dark`, `heritage_copper`, `minimalist_mono`, `monograph_ink`,
  `organic_clay`, `product_bento`, `sidebar_layout`, `signal_grid`,
  `summit_narrative`, `sunrise_mosaic`, `tide_glass`, and `two_column`.
- 22 active templates are standalone HTML documents with their own CSS:
  `aurora_studio`, `boardroom_blue`, `bold_dark_neon`, `case_study_magazine`,
  `clean_minimal`, `creative_vibrant`, `dev_terminal`, `editorial_linen`,
  `elegant_classic`, `forest_dark`, `gradient_purple`, `indigo_modern`,
  `luxury_elegant`, `modern_corporate`, `nature_green`, `navy_business`,
  `ocean_blue`, `rose_minimal`, `slate_professional`, `sunset_gradient`,
  `teal_modern`, and `tech_glassmorphism`.

The shared base is a useful compatibility foundation, but it is also a source
of coupling: templates that inherit from it share page structure, CSS, section
markup, and responsive behavior. Standalone templates provide stronger layout
independence but duplicate CSS and content conventions.

### Gallery and template selection

`portfolio/views.py` loads active templates for the gallery, homepage, and
builder. `templates/portfolio_gallery.html` presents category filters and uses
the real preview endpoint inside scaled, non-interactive iframe covers. Each
card links to the full preview and to the builder with the selected template.

The gallery currently exposes four user-facing filters: minimalist, developer,
creative, and corporate. The backend model has a fifth `latest` choice, but the
gallery does not currently display a latest filter.

## 4. Data model and template context

### Saved portfolio models

`Portfolio` is the original portfolio model. It contains:

- Basic profile data: name, title, biography, email, phone, and location.
- Social URLs: LinkedIn, GitHub, website, and Twitter.
- Original and processed profile images.
- JSON fields for skills, stats, projects, experience, and education.
- A required `PortfolioTemplate` foreign key with `PROTECT` deletion behavior.
- Publication and timestamp fields.

`PublicPortfolio` supports the authenticated/public publishing flow. It mirrors
the profile and JSON content fields, has a nullable template foreign key, a
unique username slug, publication/featured flags, and a view counter.

`PortfolioProject`, `PortfolioExperience`, and `PortfolioEducation` are optional
normalized child models. Their serializers and admin inlines exist, but the
main renderers currently read the JSON fields on `Portfolio` or
`PublicPortfolio`, not the normalized child querysets.

`UserProfile` stores account-level bio/avatar/website information separately
from the portfolio content.

### Context paths

There are three related context paths:

1. `portfolio/preview_context.py` creates sample and unsaved draft preview
   contexts.
2. `portfolio/services.py` provides `PortfolioRenderer` for saved
   `Portfolio` objects and `PublicPortfolioRenderer` for published objects.
3. `generate_template_preview_pack.py` contains a separate rich demo context
   for generating an offline preview pack.

The renderer contexts expose both direct variables and the `portfolio` object.
The common contract currently includes:

```text
portfolio
full_name, title, bio, email, phone, location
linkedin, github, portfolio_website, twitter
website, website_url, linkedin_url, github_url, twitter_url
profile_image, profile_image_url, profile_image_base64
skills, stats, projects, experience, education
template_color
```

The preview builder also creates a lightweight `SimpleNamespace` portfolio
object so templates can safely use either `{{ full_name }}` or
`{{ portfolio.full_name }}`. Draft preview values are rendered without saving;
blank drafts fall back to the fictitious Morgan Lee sample profile.

The JSON content is intentionally flexible. Normalization functions in
`preview_context.py` add compatibility aliases such as `role`/`title`/
`job_title`, `school`/`institution`, and `live_link`/`project_url`.

## 5. Rendering, preview, and public flow

### Full template preview

The main route is:

```text
GET or POST /api/template/<template_id>/preview/
```

`portfolio/views.py:template_preview`:

- Resolves an active `PortfolioTemplate` record.
- On GET, builds the complete sample context.
- On POST, parses form values and an optional uploaded image into a no-save
  draft context.
- Renders the catalog record's `template_file` with Django's
  `render_to_string`.
- Returns HTML with `Cache-Control: no-store`.
- Allows same-origin iframe embedding for gallery and builder previews.

The gallery iframe and builder preview both use this route, so the preview
endpoint is the central visual integration point for a new template.

### Saved/API portfolio flow

`portfolio/urls.py` mounts DRF routers for:

- `/api/templates/` — read-only active template catalog, search, ordering, and
  category filtering.
- `/api/portfolios/` — portfolio CRUD plus preview, download, publish, and image
  processing actions.

`PortfolioViewSet.preview` renders a saved `Portfolio` using
`PortfolioRenderer`. `public_portfolio_view` renders a published
`PublicPortfolio` using `PublicPortfolioRenderer`, increments its view count,
and serves the selected template as HTML.

If a public portfolio has no template, the public view assigns the first active
template by order as a fallback.

### User information injection

The builder form supplies active template records to Django, and browser-side
preview requests send current form values to the preview endpoint. The request
is not persisted. Saved content is injected by the renderer service from model
fields. Templates are therefore data-driven only through the common context;
there is no per-template component API or schema declaration.

## 6. Asset management

### Profile images

- Saved `Portfolio` images use `media/profiles/` and processed copies use
  `media/profiles_processed/`.
- Saved `PublicPortfolio` images use `media/portfolio_profiles/` and processed
  copies use `media/portfolio_profiles_processed/`.
- `PortfolioRenderer` and `PublicPortfolioRenderer` prefer the processed image,
  then the original image.
- For downloadable HTML, the chosen image is read and embedded as a base64
  data URI.
- For unsaved previews, uploaded PNG/JPEG/GIF/WebP images up to 5 MB are
  embedded directly as data URIs and are not stored.
- Gallery samples use an embedded SVG portrait defined in
  `portfolio/preview_context.py`.

### Image processing

`portfolio/image_processor.py` removes backgrounds using lazy-loaded `rembg`
when available, falls back to corner-color removal, creates a themed gradient,
and saves a processed image. The `TEMPLATE_THEMES` mapping is a separate manual
slug-to-color map. A new template does not automatically receive a distinct
image-processing theme; adding one requires updating that map or accepting a
fallback theme.

### Fonts, icons, and static files

- Fonts are primarily external Google Fonts linked from HTML templates.
- Icons are mostly inline SVG markup and CSS shapes; there is no icon package or
  centralized icon component.
- CSS is primarily inline in `base.html`, the shared portfolio partial, and
  individual portfolio templates.
- Static collection is configured through WhiteNoise, but the portfolio template
  pages do not currently use a centralized per-template static asset bundle.
- `preview_image` exists as a model/API field but has no current source-template
  or gallery rendering integration.

## 7. Responsive CSS, JavaScript, and animation

Responsive behavior is implemented manually in CSS:

- `templates/base.html` contains global responsive layout and reduced-motion
  conventions for the application shell.
- `_portfolio_base.html` contains shared portfolio media queries and print
  styles.
- Standalone portfolio templates define their own breakpoints, often around
  720–800 px, with layout-specific changes.
- The gallery has responsive grid breakpoints at approximately 1050, 720, and
  520 px.

JavaScript is intentionally light:

- Builder and gallery interactions are inline in their Django templates.
- `image-processor.js` handles authenticated image upload/processing,
  client-side image preview, and small status/progress UI helpers.
- There is no bundler, module graph, state-management library, or frontend test
  suite.

Animations are distributed across CSS files. The current codebase includes
transitions and a small number of keyframe animations, including the creative
marquee, terminal cursor, and sunset ticker. Reduced-motion handling is present
in the gallery and should be made a consistent requirement for future premium
designs.

## 8. Exports and downloads

The supported download endpoint is:

```text
GET /api/portfolios/<portfolio_id>/download/
```

It renders the selected saved portfolio to HTML, sets
`Content-Disposition: attachment`, and returns a filename derived from the
portfolio owner's name. Images are embedded as data URIs, making the downloaded
HTML more self-contained.

There is currently no server-side PDF export, image export, ZIP package,
static-site build, or browser screenshot export. A new template should continue
to render as a complete standalone HTML document if it must support the current
download behavior.

## 9. Recommended integration approach for 150 premium templates

The current system can scale to more templates if the stable data contract is
preserved, but adding 116 templates by copying ad hoc HTML/CSS would increase
registry drift, repeated CSS, and regression risk. Recommended approach:

### Phase A — formalize the contract before bulk production

1. Keep `PortfolioTemplate` as the public catalog model and preserve the
   existing preview/public/download routes.
2. Introduce a single authoritative template manifest/registry with slug, name,
   category, description, template path, preview metadata, layout family, and
   version. The existing management command should consume it rather than
   maintaining a long hand-edited list independently of tests.
3. Define a versioned, documented context contract for profile, links, image,
   skills, stats, projects, experience, and education. Add safe defaults for
   optional/missing fields.
4. Consolidate duplicated context and image encoding logic in
   `PortfolioRenderer`, `PublicPortfolioRenderer`, and preview builders so all
   rendering modes receive the same aliases.

### Phase B — organize premium template implementation

1. Use explicit layout families only where structural reuse is intended. A
   premium template that must be visually distinct should be standalone or use
   isolated primitives instead of silently inheriting a page layout.
2. Move reusable tokens, accessibility rules, and reset behavior into a stable
   shared layer, while keeping template-specific layout and visual direction
   isolated.
3. Store non-inline template assets under a predictable path such as
   `portfolio/static/portfolio/templates/<slug>/` and reference them with the
   `{% static %}` tag.
4. Treat 15 professional categories as catalog metadata, not as additional
   hardcoded filter branches. The gallery should render category filters from
   the available active categories.

### Phase C — validation and release

1. Add a registry consistency check: unique slug, existing template file,
   supported category, valid manifest, and required context fields.
2. Keep an all-template smoke test that renders every active record through the
   real preview endpoint.
3. Add browser-based visual checks at desktop and mobile widths, including
   overflow/viewport-fit checks, text contrast, image fallback, and link
   visibility.
4. Add accessibility checks for heading order, landmark structure, link names,
   image alternatives, keyboard focus, and reduced-motion behavior.
5. Generate and review a preview pack before activating a batch of templates.
6. Make catalog synchronization an explicit deployment/release step, or move
   the catalog into migrations/fixtures so a fresh deployment cannot serve a
   stale template database.

## 10. Potential technical risks and current limitations

### Template and data risks

- `template_file` is stored as a database string and passed to Django template
  loading. It has no explicit manifest validation or path allowlist.
- JSON fields have no versioned schema. Templates currently depend on informal
  key aliases and defensive conditionals.
- The normalized child models and JSON fields coexist, but rendering uses the
  JSON fields. Future work must not assume the child models are the source of
  truth.
- `PortfolioRenderer`, `PublicPortfolioRenderer`, preview contexts, and the
  offline preview-pack command duplicate context construction. They can drift.
- The current structural tests validate HTML strings and endpoint status, but do
  not provide browser-level visual regression, overflow, contrast, or
  accessibility coverage.
- A long manual registry and a tracked SQLite database can become inconsistent
  when a new template is added but the load command is not run.

### Asset and runtime risks

- Google Font links create an external network dependency and can produce visual
  changes or fallback typography when offline or blocked.
- Image processing depends on heavy native/ML packages and can be expensive in
  constrained deployment environments.
- Local filesystem media is not durable across many ephemeral hosting setups;
  production image storage should use persistent or object storage.
- Base64 embedding increases HTML response/download size for large images.
- There is no centralized icon or asset pipeline, so 150 designs could create
  duplicated markup and inconsistent accessibility.

### Operational/security risks

- `ALLOWED_HOSTS` is currently `['*']`.
- Settings contain a fallback secret key if `SECRET_KEY` is absent.
- The tracked SQLite database is useful for local development but is not a
  durable production database strategy.
- There is no `.github/workflows/`, Dockerfile, `railway.toml`, or documented
  automatic catalog-seeding step in the repository. Railway deployment depends
  on its external project configuration plus the Procfile/runtime files.
- The local development virtual environment is Python 3.10 while the declared
  deployment runtime is Python 3.11.

## 11. Exact files affected when adding one standard template

For a template that uses the existing context contract and no special assets,
the minimum source changes are:

1. `templates/portfolio_templates/template_<slug>.html` — add the complete
   Django template and responsive CSS.
2. `portfolio/management/commands/load_templates.py` — add the catalog record
   with name, slug, description, category, color scheme, template path, and
   order.
3. `portfolio/tests/test_previews.py` — add the template path to the complete
   render list and add a focused structure/visibility regression test when the
   design has important unique behavior.
4. `db.sqlite3` — update only if this repository intentionally commits the
   synchronized catalog database; otherwise run the catalog command during the
   release/deployment process.

Files that are conditional, not normally required:

- `portfolio/image_processor.py` — only if the template needs a distinct
  processed-image theme in `TEMPLATE_THEMES`.
- `portfolio/static/portfolio/templates/<slug>/...` — only if the design uses
  external local CSS, JavaScript, fonts, or image assets.
- `portfolio/preview_context.py` — only if the design requires a new shared
  data field; standard templates should use the existing context contract.
- `portfolio/services.py` — only if the renderer contract itself must change;
  avoid template-specific branching here.
- `templates/portfolio_gallery.html` — only if gallery behavior or metadata
  presentation changes; a normal catalog record is picked up automatically.
- `portfolio/models.py`, migrations, serializers, or URLs — not required for a
  standard visual template and should not be changed merely to register one.

## 12. Design handoff guidance

Design specifications should describe each premium template in terms the
existing renderer can satisfy:

- unique slug, display name, category, and intended audience;
- page geometry and responsive breakpoints;
- required sections and their behavior when data is missing;
- typography and asset requirements;
- profile-image treatment and fallback behavior;
- link/contact visibility and accessible labels;
- motion, hover, and reduced-motion behavior;
- whether the template must support print and standalone HTML download.

The implementation phase should begin only after those specifications are
approved. The safest first implementation milestone is one fully specified
template integrated through the existing preview, saved render, public render,
download, gallery, and automated smoke-test paths before creating a larger
batch.

