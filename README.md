# cicd-test

![CI](https://github.com/hisamist/cicd-test/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python/Flask project demonstrating CI/CD best practices with automated linting, testing, and coverage enforcement. The app provides a delivery order pricing API with promo code support and surge pricing.

## Features

- **Pricing engine** — calculates order totals with delivery fees, promo codes, and surge multipliers
- **REST API** — Flask endpoints to simulate and create orders, validate promo codes
- **Exercise utilities** — string helpers, validators (email, password, age), and sorting utilities
- **CI/CD pipeline** — GitHub Actions runs lint + tests + coverage on every push/PR

## Project Structure

```
src/
├── database.py          # In-memory orders store and promo codes
├── pricing/
│   ├── price.py         # Pricing logic (delivery fee, promo, surge, order total)
│   └── routes.py        # Flask API routes
└── exercise/
    ├── utils.py          # capitalize, slugify, clamp, sort_students, calculateAverage
    └── validators.py     # is_valid_email, is_valid_password, is_valid_age

tests/
├── unit/                # Unit tests for pricing and exercise modules
└── integration/         # Integration tests for API routes
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Hello World |
| GET | `/health` | Health check |
| POST | `/orders/simulate` | Simulate order total without saving |
| POST | `/orders` | Create and persist an order |
| GET | `/orders/<id>` | Retrieve an order by ID |
| POST | `/promo/validate` | Validate a promo code |

### Example — Simulate an order

```bash
curl -X POST http://localhost:5000/orders/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{"price": 12.5, "quantity": 2}],
    "distance": 5,
    "weight": 3,
    "promoCode": "BIENVENUE20",
    "hour": "12:30",
    "dayOfWeek": "lundi",
    "currentDate": "2026-04-09"
  }'
```

## Promo Codes

| Code | Type | Value | Min Order | Expires |
|------|------|-------|-----------|---------|
| `BIENVENUE20` | percentage | 20% | 15.00 | 2026-12-31 |
| `PROMO5` | fixed | -5 | 10.00 | 2026-12-31 |
| `PROMO10` | fixed | -10 | 30.00 | 2026-12-31 |

## Surge Pricing

Delivery fees are multiplied based on the time and day:

| Day | Time | Multiplier |
|-----|------|-----------|
| Sunday | 10:00–22:00 | ×1.2 |
| Mon–Thu | 12:00–13:30 | ×1.3 |
| Mon–Thu | 19:00–21:00 | ×1.5 |
| Fri–Sat | 19:00–22:00 | ×1.8 |
| Any | Outside 10:00–22:00 | ×0 (closed) |

## Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install with dev dependencies
pip install .[dev]

# Install pre-commit hooks
pre-commit install
```

## Running the App

```bash
python -m flask --app src/pricing/routes.py run
```

## Development Tasks

```bash
task lint       # Check code style with Ruff
task lint-fix   # Auto-fix linting issues
task format     # Reformat code
task test       # Run all tests
task cov        # Run tests with coverage (fails if < 80%)
```

## CI/CD Pipeline

GitHub Actions runs on every push to `master`, `main`, or `develop`, and on all pull requests:

1. Checkout & set up Python 3.11
2. Install dependencies (`pip install .[dev]`)
3. Run linter (`task lint`)
4. Run tests with coverage — fails if coverage drops below **80%** (`task cov`)

## Pre-commit Hooks

Configured hooks run automatically before each commit:

- Trim trailing whitespace
- Ensure files end with a newline
- Validate YAML syntax
- Block large file commits
- Ruff lint + format
