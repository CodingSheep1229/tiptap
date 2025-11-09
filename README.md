# TipTap - Restaurant Tip Tracker

TipTap is a web application that tracks restaurant charges and automatically detects tip overcharges. When you make a restaurant purchase, the initial charge appears as "pending" in your bank. After recording your intended tip, TipTap monitors when the transaction finalizes and alerts you if the restaurant charged more than expected.

## Features

- 🔗 **Plaid Integration** - Connect your bank account securely via Plaid
- 📊 **Transaction Tracking** - Monitor pending and posted restaurant transactions
- 💰 **Tip Recording** - Record your intended tip amounts
- ⚠️ **Overcharge Detection** - Automatically detect when restaurants overcharge on tips
- 🧪 **Sandbox Testing** - Test the full flow with Plaid's sandbox environment

## Project Structure

```
tiptap/
├── backend/
│   ├── routes/          # API route handlers
│   │   ├── plaid_routes.py
│   │   ├── transaction_routes.py
│   │   ├── tip_routes.py
│   │   └── sandbox_routes.py
│   ├── services/        # Business logic
│   │   └── transaction_service.py
│   ├── config.py        # Application configuration
│   ├── database.py      # Database setup and helpers
│   ├── models.py        # Pydantic models
│   └── plaid_client.py  # Plaid API client
├── frontend/
│   └── index.html       # Single-page web interface
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md
```

## Setup

### Prerequisites

- Python 3.8+
- A Plaid account (sign up at https://dashboard.plaid.com)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd tiptap
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Plaid credentials:
   ```
   PLAID_CLIENT_ID=your_client_id_here
   PLAID_SECRET=your_secret_here
   PLAID_ENV=sandbox
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Open the frontend**
   - Open `frontend/index.html` in your web browser
   - Or serve it with: `python -m http.server 5173` (from the frontend directory)

## Usage

### Testing with Sandbox

1. **Create a Test Item** - Click "Create Test Item (50 pending txns)"
2. **Record a Tip** - Enter tip amount for a pending transaction
3. **Simulate Update** - Click "Simulate Transaction Update" to test overcharge detection
4. **Check Results** - View the "Tip Records" table for verification status

## API Endpoints

- `POST /link/token` - Create Link token
- `POST /exchange` - Exchange public token
- `GET /transactions/pending` - Get pending transactions
- `POST /tips` - Record tip
- `GET /tips` - Get tip records
- `POST /sync` - Manual sync
- `POST /sandbox/create_test_item` - Create test data
- `POST /sandbox/simulate_transaction_update` - Simulate updates

## Tech Stack

- **Backend**: FastAPI, Python 3.8+
- **Database**: SQLite with aiosqlite
- **API**: Plaid API
- **Frontend**: Vanilla JavaScript

## License

MIT
