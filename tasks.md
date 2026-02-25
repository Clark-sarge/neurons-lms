## Project tasks overview

This file tracks **high-level tasks** for the Neurons LMS and gives agents quick context when starting work.

- **Status values**: `todo`, `in-progress`, `done`, `blocked`
- **Owners**: GitHub username, initials, or `agent`
- **Scope**: keep this focused on milestones and non-trivial work (not tiny one-off tweaks).

## How to use this file

- **When starting work**: skim the sections below to understand current priorities and what’s already done.
- **When adding a task**: add it under the appropriate section with a short, action-oriented description.
- **When finishing a task**: move it to the **Completed tasks** section and update the status to `done`.
- **For blocked work**: mark `blocked` and briefly note why.

Try to keep entries brief—1–2 lines each.

### Task entry format

Use this format for individual tasks:

- **[status]** Short description *(owner, date)* — optional extra notes

Example:

- **[in-progress]** Implement adaptive quiz scheduling *(agent, 2026-02-23)* — depends on analytics pipeline

---

## Current priorities

- **[todo]** Flesh out LMS feature roadmap and milestones *(agent)*  
- **[todo]** Design core learner dashboard UI and navigation *(agent)*  
- **[todo]** Define initial AI-assisted features (recommendations, feedback, pacing) *(agent)*  

---

## Backend / data model

- **[todo]** Expand user model to capture learner profile data (goals, preferences, constraints) *(agent)*  
- **[todo]** Model learning activities and outcomes to support personalization *(agent)*  
- **[todo]** Add basic analytics events (viewed module, completed content, quiz results) *(agent)*  

---

## Frontend / UX

- **[todo]** Create responsive layout for student, instructor, and admin views *(agent)*  
- **[todo]** Implement course list and course detail pages suitable for personalization *(agent)*  
- **[todo]** Improve user management UI for bulk operations and search/filter *(agent)*  

---

## AI / personalization

- **[todo]** Identify key decision points where AI will assist learners (what to study next, pacing, feedback) *(agent)*  
- **[todo]** Design API boundaries for AI services (recommendations, hints, content generation) *(agent)*  
- **[todo]** Draft evaluation metrics for learner outcomes and system effectiveness *(agent)*  

---

## DevOps / environment

- **[todo]** Add `.env` template documenting required environment variables *(agent)*  
- **[todo]** Add simple local setup script or Makefile/PowerShell script for common commands *(agent)*  
- **[todo]** Set up basic test suite for core models and views *(agent)*  

---

## Completed tasks

- **[done]** Document project purpose and high-level roles in `README.md` *(agent, 2026-02-23)*  
- **[done]** Set up Python virtual environment and dependency pinning for Django-based LMS *(agent, 2026-02-23)*  
- **[done]** Add management command and documentation for test accounts and sample course *(agent, 2026-02-23)*  
- **[done]** Create and document project task tracker in `tasks.md` *(agent, 2026-02-23)*  
- **[done]** Update login flow to use username field and show friendly error message on failed login *(agent, 2026-02-23)*  

