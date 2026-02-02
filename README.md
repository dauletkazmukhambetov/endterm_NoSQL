# Car Store

A simple full-stack car store built with FastAPI, MongoDB, and vanilla HTML/CSS/JavaScript.

## Features

- **Cars**: Browse, add, edit, delete cars
- **Users**: Sign up and login
- **Orders**: Place orders, view order history

## Tech Stack

- **Backend**: FastAPI, Motor (async MongoDB), Pydantic
- **Database**: MongoDB (database: `car_store`)
- **Frontend**: HTML, CSS, JavaScript

## Project Structure

```
endterm/
├── app/
│   ├── main.py
│   ├── crud.py
│   ├── db.py
│   └── schemas.py
├── src/
│   ├── index.html
│   ├── cars.html
│   ├── auth.html
│   ├── orders.html
│   ├── api.js
│   ├── nav.js
│   └── style.css
└── requirements.txt
```

## Collections

- **cars** – make, model, year, price, mileage, color, condition, description
- **users** – name, email, password
- **orders** – car_id, user_id, price, status

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /cars/ | List cars (filters: make, condition, min_price, max_price, min_year, max_year) |
| POST | /cars/ | Create car |
| GET | /cars/{id} | Get car |
| PUT | /cars/{id} | Update car |
| DELETE | /cars/{id} | Delete car |
| GET | /cars/stats/aggregation | Multi-stage aggregation stats (by make, condition, price range) |
| POST | /users/ | Sign up |
| POST | /users/login/ | Login |
| POST | /orders/ | Create order |
| GET | /orders/?user_id= | Get user orders |

## Running

**Prerequisites:** Python 3.10+, MongoDB running locally (default: `mongodb://localhost:27017`)

1. Install dependencies: `pip install -r requirements.txt`
2. Run API: `uvicorn app.main:app --reload --port 8000`
3. Serve frontend: `cd src && python -m http.server 5500`

- **Frontend**: http://127.0.0.1:5500
- **API Docs**: http://127.0.0.1:8000/docs

Optional `.env`:
```
MONGODB_URI=mongodb://localhost:27017
DB_NAME=car_store
```

## License

MIT
