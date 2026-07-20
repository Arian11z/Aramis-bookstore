# Aramis Bookstore

A full-featured online bookstore web application built with Django, featuring book ratings, customer reviews, and Persian sentiment analysis powered by natural language processing.

## Overview

Aramis Bookstore is a complete e-commerce style platform for browsing, searching, and purchasing books online. Beyond standard catalog and cart functionality, the platform includes an intelligent sentiment analysis system that automatically classifies customer reviews as positive, negative, or neutral using Persian NLP techniques.

## Features

### Book Catalog
- Detailed book listings with title, author, description, price, ISBN, page count, and stock
- Cover image upload support
- Category-based organization
- Automatic calculation of average ratings and review counts

### Search and Filtering
- Full-text search across title, author, and description
- Filter by author, category, price range, and minimum rating
- Sorting by newest, oldest, price, and title
- Paginated results

### Ratings and Reviews
- Five-star rating system with one rating per user per book
- Text review submission with edit support
- Automatic sentiment analysis on submitted reviews
- Sentiment classification displayed alongside each review

### Shopping Cart
- Add, remove, and update item quantities
- Real-time stock validation
- Automatic total price calculation

### User Accounts
- Registration, login, and logout
- User profile page displaying personal review and rating history
- Access control for authenticated actions

### Admin Panel
- Full management of books, categories, reviews, ratings, and carts
- Search and filter tools within the admin interface

### Sentiment Analysis
The project implements three progressively more accurate approaches to Persian sentiment analysis:

1. Keyword-based analysis using a curated list of positive and negative Persian words
2. Hazm-based analysis with normalization, tokenization, and stemming
3. Hazm combined with the PerSent lexicon, containing over 26,000 weighted Persian sentiment words

## Technology Stack

**Backend**
- Django 5.x
- Python 3.x
- SQLite
- Pillow (image handling)
- Hazm (Persian NLP)

**Frontend**
- HTML5
- CSS3
- Vazirmatn font

## Project Structure

```
bookstore/
├── accounts/            User authentication and profile app
├── books/                Book catalog, reviews, ratings, cart, and sentiment analysis app
├── bookstore/            Project configuration
├── static/               CSS and static assets
├── templates/            HTML templates
├── media/                Uploaded book cover images (not tracked in version control)
└── manage.py
```

## Installation

### Prerequisites
- Python 3.10 or higher
- pip

### Setup

Clone the repository:

```bash
git clone https://github.com/Arian11z/Aramis-bookstore.git
cd Aramis-bookstore
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install django pillow hazm requests
```

Apply database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create an administrator account:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.
The admin panel will be available at `http://127.0.0.1:8000/admin/`.

## Database Schema

The application uses seven primary models:

| Model | Description |
|-------|-------------|
| Category | Book genre or classification |
| Book | Core book information and metadata |
| Review | User-submitted text reviews with sentiment analysis |
| Rating | User-submitted star ratings (1-5) |
| Cart | Per-user shopping cart |
| CartItem | Individual items within a cart |
| User | Django's built-in authentication model |

## Sentiment Analysis Details

The sentiment analysis module processes review text through the following pipeline:

1. Text normalization using Hazm's Normalizer
2. Tokenization into individual words
3. Lookup of each token against the PerSent sentiment lexicon
4. Weighted scoring based on lexicon values
5. Classification into positive, negative, or neutral categories with a confidence score

## License

This project was developed for educational purposes.

## Author

Developed as part of an internship project.