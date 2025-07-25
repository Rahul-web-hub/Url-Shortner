# URL Shortener Service

A lightweight Flask application that mimics services like Bitly or TinyURL by providing short, memorable links for long URLs. This project focuses on simplicity, thread safety, and easy deployment—perfect for a quick demo, learning exercise, or small-scale use.

## Table of Contents
* [Overview](#overview)
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Installation & Setup](#installation--setup)
* [Usage](#usage)
* [Implementation Details](#implementation-details)
* [Testing](#testing)
* [Deployment](#deployment)
* [Notes & AI Usage](#notes--ai-usage)
* [License](#license)

---
## Notes & AI Usage
* I used AI tools sparingly for wording suggestions and to tidy up comments—purely for helpful guidance. All core logic, testing, and design choices were hand-crafted and reviewed manually.
---
## Overview
This service allows users to:

* Shorten a long URL into a 6‑character code.
* Redirect visitors from the short URL to the original address.
* Track click counts and view basic analytics per code.

All data is stored in an in-memory Python dictionary, making it easy to understand and extend. Thread locks ensure concurrent requests are handled safely.

---

## Features
* RESTful API with `JSON` responses.
* Automatic code reuse: shortening the same URL returns the same code.
* Click tracking: each redirect increments a counter.
* Simple validation: only well-formed `HTTP`/`HTTPS` URLs are accepted.

---

## Prerequisites
* Python 3.8 or higher
* Git (for cloning)
* (Optional) A virtual environment tool: `venv`, `virtualenv`, etc.

---

## Installation & Setup

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/url-shortener.git
cd url-shortener
```

### 2. (Optional) Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python -m flask --app app.main run
```
By default, the service listens on [http://localhost:5000](http://localhost:5000).

---

## Usage

Use any HTTP client (cURL, Postman, browser) to interact with the API.

### Shorten a URL

**POST** `/api/shorten`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "url": "https://www.example.com/some/long/path"
}
```

**Response (201 Created):**
```json
{
  "short_code": "abc123",
  "short_url": "http://localhost:5000/abc123"
}
```

### Redirect

Visit the short link in your browser or via cURL:

**GET** `/abc123`

Your client will receive a **302 Redirect** to the original URL.

### Get Analytics

**GET** `/api/stats/abc123`

**Response (200 OK):**
```json
{
  "url": "https://www.example.com/some/long/path",
  "clicks": 5,
  "created_at": "2025-07-25T12:34:56.789012"
}
```

---

## Implementation Details

### Project Structure
```
url-shortener/
├── app/
│   ├── main.py       # Flask app with endpoints
│   ├── models.py     # URLMapping class
│   └── utils.py      # Helper functions (code gen, URL validation)
├── tests/
│   └── test_basic.py # Pytest suite covering core features
├── requirements.txt  # Project dependencies
└── README.md         # This file
```

### Data Model

**URLMapping:** A class tracking:
- `original_url` (str)
- `created_at` (ISO timestamp)
- `clicks` (int)

**Methods:**
- `increment_clicks()`
- `to_dict()` → JSON‑friendly dict

### Utilities

- `generate_short_code(existing_codes, length=6)`: Creates a unique alphanumeric code.
- `is_valid_url(url)`: Uses a robust validation library to ensure correct HTTP/HTTPS URL format.

### Thread Safety

A global `threading.Lock()` (`db_lock`) wraps all reads/writes to the in-memory store, preventing concurrent access issues in a multi-threaded server.

---

## Testing

Run the full test suite with:

```bash
pytest
```

The tests cover:
- Health endpoints
- URL shortening logic
- Redirect behavior and click counting
- Error handling (invalid input, missing codes)
- Code reuse on duplicate URLs

---
