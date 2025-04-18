# VotingApp

## Overview
An Indian-style electronic voting system built with Streamlit, featuring voter authentication, candidate selection, and admin dashboards.

## Installation
1. Clone the repo: `git clone https://github.com/Abhishekteli-21/VotingApp.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`

## Deployment on OpenShift
1. Push updates to GitHub.
2. In OpenShift Web Console, use "+Add" > "From Git" with URL: `https://github.com/Abhishekteli-21/VotingApp.git`.
3. Set application name (e.g., `voting-app`) and create a route.
4. Monitor build logs for success.

## Notes
- Ensure `requirements.txt` includes all dependencies.
- WSGI compatibility added via Flask for OpenShift.