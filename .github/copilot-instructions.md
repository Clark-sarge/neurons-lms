# Copilot Instructions for neurons-lms

## Project Overview
- **neurons-lms** is a Django-based Learning Management System (LMS) with a modular structure.
- Main app: `custom_lms/lms_app` containing models, views, and business logic.
- Key models: `Course`, `Module`, and `Content` (see `models.py`).
- Modular content: Courses have modules (can be nested), each module can have multiple content items (files, links, quizzes, discussions).

## Architecture & Patterns
- **App structure:**
  - `custom_lms/` is the Django project root (settings, URLs, WSGI/ASGI).
  - `lms_app/` is the main app for LMS features.
- **Models:**
  - `Course` → `Module` (can be nested via `parent`) → `Content` (polymorphic by type).
  - Use `related_name` for reverse relations (e.g., `course.modules`).
- **Views:**
  - Use Django's class-based and function-based views.
  - Permissions: Use `@login_required` and check `request.user.role` for access control.
- **Templates:**
  - Templates are referenced in views (e.g., `home.html`, `course_list.html`).
  - Bootstrap and FontAwesome are used for UI (see inline HTML in some files).

## Developer Workflows
- **Run server:**
  - `python manage.py runserver`
- **Migrations:**
  - `python manage.py makemigrations`
  - `python manage.py migrate`
- **Create superuser:**
  - `python manage.py createsuperuser`
- **Testing:**
  - No explicit test files found; add tests in `lms_app/tests.py`.
- **Static/media files:**
  - File uploads are stored in `content_files/` (see `Content.file`).

## Conventions & Customizations
- **User roles:**
  - Custom roles (`student`, `instructor`, `admin`) checked in views for permissions.
- **Settings:**
  - Uses `python-decouple` for environment variables (see `settings.py`).
  - `ALLOWED_HOSTS` is set to `['*']` for development.
- **External dependencies:**
  - Django, Pillow, python-decouple (see `requirements.txt`).

## Integration Points
- **Admin:**
  - Standard Django admin at `/admin/`.
- **User management:**
  - Custom logic in `views.py` for user listing and permissions.
- **Content types:**
  - Extend `Content` model for new types if needed.

## Examples
- To get all modules for a course: `course.modules.all()`
- To get all content for a module: `module.contents.all()`

---

**Update this file if you add new apps, change model relationships, or introduce new developer workflows.**
