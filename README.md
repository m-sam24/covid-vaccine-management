# COVID Vaccine Management

A small vaccination booking system: citizens register, book a vaccine slot at a hospital, and download a vaccination certificate. Admins manage hospitals, dose stock and users.

- **Backend:** FastAPI + MySQL (`backend/`)
- **Frontend:** React + TypeScript + Vite (`frontend/`)

```
.
├── backend/
│   ├── app.py              # FastAPI app (all API routes)
│   ├── db.py               # MySQL connection + table creation
│   ├── requirements.txt
│   ├── .env.example        # template for backend/.env (database login)
│   ├── start-mysql.sh      # helper for a local MySQL on port 3307 (macOS/Homebrew)
│   ├── stop-mysql.sh
│   └── Covid project.py    # original command-line version (not used by the API)
└── frontend/
    ├── src/
    │   ├── api.ts          # typed client for every backend endpoint
    │   ├── types.ts        # request/response types
    │   ├── components/     # table, toast, form helpers
    │   └── pages/          # one component per tab
    └── vite.config.ts      # dev server + /api proxy to the backend
```

## Prerequisites

- Python 3.9+
- Node.js 18+ and npm
- MySQL 8

## 1. Start MySQL

You need a running MySQL server. The backend creates the `vaccine_management` database and its tables automatically on startup.

The connection is configured in `backend/.env`, which is not committed. Create it from the template:

```sh
cp backend/.env.example backend/.env
```

Then set your MySQL login in it:

| Variable      | Default in template  |
| ------------- | -------------------- |
| `DB_HOST`     | `127.0.0.1`          |
| `DB_PORT`     | `3307` (use `3306` for a standard MySQL install) |
| `DB_USER`     | `root`               |
| `DB_PASSWORD` | *(required)*         |
| `DB_NAME`     | `vaccine_management` |

Real environment variables override the values in `.env`.

> `backend/start-mysql.sh` and `stop-mysql.sh` start/stop a Homebrew `mysql@8.4` instance on port 3307 using a config file at `/Users/sam/mysql.cnf`. They only work on that machine. Everyone else should run their own MySQL and set the variables above.

## 2. Run the backend

```sh
cd backend
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Check it at http://localhost:8000. Interactive API docs are at http://localhost:8000/docs.

## 3. Run the frontend

In a second terminal:

```sh
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

In development, the Vite dev server forwards every request under `/api/*` to `http://localhost:8000`, so the backend address doesn't need to be configured. To use a backend somewhere else:

- `BACKEND_URL=http://host:port npm run dev` changes where the dev server forwards requests.
- `VITE_API_URL=http://host:port` (set at build time) makes the frontend call the API directly instead. The backend already allows cross-origin requests.

A badge in the header shows whether the API is reachable.

## Using the app

1. **Hospitals** (admin): click *Insert sample hospitals*, or add your own.
2. **Doses** (admin): add a dose for a hospital ID with a date, price and the capacity of each of the 4 slots.
3. **Register**: register a person by Aadhaar number, name, age and phone.
4. **Book Vaccine**: pick a slot from the table and enter the Aadhaar number. The first booking is dose 1, the second is dose 2.
5. **Users** (admin): *Mark vaccinated* records the dose as given.
6. **Certificate**: view the dose 1 or dose 2 certificate by Aadhaar number.

## Production build

```sh
cd frontend
npm run build      # type-checks, then outputs static files to frontend/dist
npm run preview    # serve the build locally
```

`npm run preview` doesn't forward `/api` to the backend. Build with `VITE_API_URL` set to the backend URL, or serve `dist/` behind a reverse proxy that sends `/api` to the backend.

## API overview

| Method | Path                        | Purpose                          |
| ------ | --------------------------- | -------------------------------- |
| GET    | `/hospitals`                | List hospitals                   |
| POST   | `/hospitals`                | Add hospital                     |
| PUT    | `/hospitals/{h_id}`         | Update phone / doctor            |
| POST   | `/hospitals/dummy`          | Insert sample hospitals          |
| GET    | `/doses`                    | List doses                       |
| GET    | `/doses/slots`              | Remaining capacity per slot      |
| POST   | `/doses`                    | Add dose                         |
| GET    | `/users`                    | List users                       |
| GET    | `/users/phone/{phone}`      | Find user by phone               |
| POST   | `/users`                    | Register user                    |
| PUT    | `/users/{adharno}`          | Update user                      |
| DELETE | `/users/{adharno}`          | Delete user                      |
| POST   | `/vaccines/book`            | Book dose 1 or dose 2            |
| PUT    | `/certificates/{adharno}`   | Mark next dose as given          |
| GET    | `/certificates/{adharno}?dose=1\|2` | Get certificate          |
