# F1 Fan Hub

F1 Fan Hub is a Django web application for Formula 1 fans.  
The project was developed as an academic full-stack web application and includes a product catalogue, role-based dashboards, simulated premium membership, wishlist, recently viewed products, AJAX reviews, and a simulated cart and checkout system.

## Project Purpose

The goal of the application is to provide a Formula 1 themed e-commerce and fan-platform experience while demonstrating:

- Django app structure
- interconnected database models
- role-based user access
- responsive front-end design
- modular HTML, CSS, and JavaScript
- client-side and server-side validation
- secure development practices
- deployment-ready configuration

## Main Features

### Public / Visitor Features
- Homepage with featured products
- Next F1 race widget using API data
- Driver and team carousels
- Product catalogue browsing
- Product detail pages
- About, Contact, and FAQ pages

### Registered User Features
- User registration and login
- Profile page with editable information
- Wishlist
- Recently viewed products
- Cart and simulated checkout
- Order history
- Product reviews with AJAX updates
- User dashboard

### Premium User Features
- Upgrade to premium membership
- Cancel premium membership
- Access premium-only products
- Premium dashboard
- Premium points system
- Redeem discount rewards
- Join raffle entries for ticket rewards

### Admin Features
- Django admin panel
- Admin dashboard
- Platform statistics
- Product, category, review, and order management

## Project Structure

The project is separated into multiple Django apps:

- `accounts` → authentication, profile, premium membership, rewards
- `catalog` → products, categories, wishlist, recently viewed
- `cart` → cart, checkout, orders
- `reviews` → product reviews and AJAX review submission
- `dashboard` → visitor, user, premium, and admin dashboards
- `config` → global settings and URL routing

## Development Approach

The application was designed using a modular approach:

- **HTML** is separated by feature/page
- **CSS** is separated by feature/page, with a shared base stylesheet
- **JavaScript** is separated by feature/page, with a shared base script
- **Django apps** are organized by functionality
- URL routing uses **namespaces** such as `accounts:view`, `catalog:view`, `cart:view`, and `dashboard:view`

This structure improves:
- maintainability
- readability
- feature separation
- reuse of shared layouts and scripts

## Front-End Approach

The interface uses:

- custom responsive CSS
- a shared global theme in `base.css`
- dark mode support
- Bootstrap CDN for framework support
- modular page-level JavaScript
- `querySelector` / `querySelectorAll` instead of `getElementById`
- deferred scripts for better loading behavior

## Database Design

The project uses multiple interconnected Django models.

Examples include:

- `User` ↔ `Profile`
- `User` ↔ `PremiumSubscription`
- `Category` ↔ `Product`
- `User` ↔ `Wishlist`
- `User` ↔ `RecentlyViewed`
- `Cart` ↔ `CartItem`
- `Order` ↔ `OrderItem`
- `User` ↔ `Review` ↔ `Product`
- `User` ↔ `DiscountReward`
- `User` ↔ `RaffleEntry`

This satisfies the requirement for interconnected models and supports the business logic of the app.

## Security / Validation Approach

The application includes several security and validation practices:

- Django ORM is used instead of raw SQL, helping protect against SQL injection
- CSRF protection is enabled through Django middleware
- Django templates escape output by default, reducing XSS risk
- Login-protected views use `@login_required`
- Client-side validation is used in forms such as Contact
- Server-side validation is used in Django forms and model logic
- Password validation is enforced during registration
- Premium-only actions check active subscription status

## Simulated Commerce Note

This project **does not use real payments**.

The following features are simulated for academic/demo purposes:
- premium subscription payment
- checkout/payment flow
- reward redemption
- raffle entry purchases

## Demo User Credentials

Use these accounts for testing:

- **Regular user:** `regularuser` / `Regular123!`
- **Premium user:** `premiumuser` / `Premium123!`
- **Admin user:** `adminuser` / `Admin123!`
- **Test user:** `testuser` / `Test123!`

> If the database is empty in deployment, run the seed commands first.

## Installation (Local)

### 1. Create a virtual environment
```bash
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_demo_users
.\.venv\Scripts\python.exe manage.py seed_f1_products
.\.venv\Scripts\python.exe manage.py runserver