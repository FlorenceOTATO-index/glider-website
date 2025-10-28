Glider Website
==============

A lightweight web application designed to manage and display mission-file workflows for underwater gliders. Built with **Python (Flask/Dash)** and simple frontend assets, the application streamlines mission planning, deployment tracking, and data post-processing for glider operations.

Background
----------

This project is developed in support of the research group led by Professor [Donglai Gong](https://www.vims.edu/about/directory/faculty/gong_d.php) at the Virginia Institute of Marine Science (VIMS). Gong’s group leverages autonomous underwater gliders to study dynamic processes in the mid-Atlantic coastal ocean—such as water-mass exchange, salinity/temperature variability, and shelf-break front behavior.

The glider missions generate specialized files (navigation logs, sensor payload outputs, deployment metadata) that require efficient organization, visualization, and delivery to both the field team and the broader research community. The **Glider Website** application is intended to fill that operational and scientific gap.

Purpose
-------

The purpose of this project is to:

* Provide a **user-friendly web interface** for mission-file upload, tracking, and archival.
* Enable quick **visual inspection** of glider mission metadata (start/end times, waypoints, sensor payloads, mission status).
* Support downstream workflows such as **data export**, **sensor metadata reconciliation**, and **integration** with glider-fleet databases.
* Facilitate better collaboration between oceanographic field teams, modelers, and data analysts by offering a **shared mission-metadata portal**.

Features
--------

* Upload, view, and manage glider mission files (e.g., navigation logs, payload summaries).
* A clean UI optimized for marine-operations users (field staff, engineers, scientists).
* Ready for deployment on platforms such as Heroku or other PaaS.
* Extensible architecture: easy to add new data-views and mission types.

Getting Started
---------------

### Prerequisites

* Python 3.9+
* pip (Python package manager)

### Installation

Clone this repository:

```bash
git clone https://github.com/FlorenceOTATO-index/glider-website.git
cd glider-website
pip install -r requirements.txt
```

Project Structure
-----------------
<pre>
glider-website/
├── App.py             # Main application entry point
├── assets/            # Static assets (CSS, JS, images)
├── pages/             # Dash page components
├── requirements.txt   # Python dependencies
├── Procfile           # Deployment configuration
└── .gitignore         # Git ignored files and folders
</pre>

