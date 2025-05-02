# Screenplay Superstore

## Overview
**Screenplay Superstore** operates as a Django-based e-commerce solution to sell virtual movie experiences from 2009 to 2024. The platform enables users to search for and order movie experiences from an administrator dashboard that allows staff to handle orders. The project employs a modern design with CSS styling and achieves 99% testing coverage.

### Design
- **Models**:
  - `Category`: Represents years (2009–2024), linked to products.
  - `Product`: Stores movie details (name, description, price, category, location).
  - `Order`: Tracks user purchases (user, product, quantity, order_date).
- **Dataset**: Sourced from `movies_2009_2024_clean.csv`, available at [https://www.kaggle.com/datasets/harios/box-office-data-1984-to-2024-from-boxofficemojo].
- **Architecture**: Follows Django’s MVT pattern, with templates styled using inline CSS for a card-based UI.

### Data Cleaning
The original dataset (`boxoffice_data_2024.csv`) contained lots of entries:
- **Filtering**: Dataset was filtered down to 3200 row by electing movie from 2009 to 2024 and multiple entries for the same movie title were removed by enforcing unique constraints on the `Product` model (`unique_together` on `name` and `category`).
- **Inconsistencies**: Missing or malformed fields (e.g., price, description) were handled by setting default values (e.g., price=0) and generating descriptions ("Experience the magic of [Title]!").
- **Categories**: Extracted years as categories (2009–2024), resulting in 16 distinct categories.
- **Result**: The cleaned dataset (`movies_2009_2024_clean.csv`) contains ~3200 unique products, loaded via a custom management command (`load_data`).

### Development
- **Tools**: Developed using PyCharm Community Edition, Python 3, and Django 5.
- **Challenges**:
  - Resolved duplicate dataset entries via migrations.
  - Implemented a secure POST-based logout to fix a 405 error.
  - Integrated Chart.js for dynamic order visualization in the admin dashboard.
- **Testing**: Achieved 99% coverage with tests for models, views, search, and authentication.

### Implementation
- **Features**:
  - Product listing with the title "Screenplay Superstore".
  - Search by title/description.
  - Detailed product pages and ordering (authenticated users only).
  - Staff-only admin dashboard with order lists and a Chart.js bar chart.
- **Styling**: Used inline CSS for a consistent, modern look with cards, shadows, and a dark blue header.
- **Deployment**: Ready for deployment with SQLite or PostgreSQL.
- **Testing**: Certain tests were conducted through pytest.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Muzaffar1260/screenplay-superstore.git
