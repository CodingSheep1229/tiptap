# TipTap - Restaurant Tip Tracker

TipTap is a web application that tracks restaurant charges and automatically detects tip overcharges. When you make a restaurant purchase, the initial charge appears as "pending" in your bank. After recording your intended tip, TipTap monitors when the transaction finalizes and alerts you if the restaurant charged more than expected.

## Features

- 🔗 **Plaid Integration** - Connect your bank account securely via Plaid
- 📊 **Transaction Tracking** - Monitor pending and posted restaurant transactions
- 💰 **Tip Recording** - Record your intended tip amounts
- ⚠️ **Overcharge Detection** - Automatically detect when restaurants overcharge on tips
- 🧪 **Sandbox Testing** - Test the full flow with Plaid's sandbox environment
- ✨ **Modern UI** - Beautiful React interface with Tailwind CSS

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
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API service layer
│   │   ├── App.jsx      # Main app component
│   │   └── main.jsx     # Entry point
│   ├── package.json     # Frontend dependencies
│   └── vite.config.js   # Vite configuration
├── main.py              # Backend entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md
```

## Setup

### Prerequisites

- Python 3.8+
- Node.js 16+ and npm
- A Plaid account (sign up at https://dashboard.plaid.com)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd tiptap
   ```

2. **Backend Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env and add your Plaid credentials
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Configure Environment**
   
   Edit `.env` and add your Plaid credentials:
   ```
   PLAID_CLIENT_ID=your_client_id_here
   PLAID_SECRET=your_secret_here
   PLAID_ENV=sandbox
   ```

### Running the Application

You need two terminal windows:

**Terminal 1 - Backend:**
```bash
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser!

## Usage

### Testing with Sandbox

1. **Create Test Data**
   - Click "Create Test Item (50 txns)" to create a test bank account
   - This uses Plaid's `user_transactions_dynamic` test user

2. **Record a Tip**
   - Enter the tip amount for any pending transaction
   - Click "Record Tip"

3. **Simulate Transaction Update**
   - Click "Simulate Transaction Update" to test overcharge detection
   - Plaid will move pending → posted and increment one transaction by $1

4. **Check Results**
   - View the "Tip Records" table
   - ✅ **VERIFIED** - Tip matches expectation
   - ⚠️ **OVERCHARGED** - Restaurant charged more than expected

### Using with Real Bank

1. Click "Connect Bank"
2. Select your bank (or "First Platypus Bank" for testing)
3. For sandbox: username = `user_transactions_dynamic`, any password
4. Click "Sync" to fetch transactions
5. Record tips for pending charges
6. When transactions finalize, overcharges are automatically detected

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /link/token | Create Link token |
| POST | /exchange | Exchange public token |
| GET | /transactions/pending | Get pending transactions |
| POST | /tips | Record tip |
| GET | /tips | Get tip records |
| POST | /sync | Manual sync |
| POST | /sandbox/create_test_item | Create test data |
| POST | /sandbox/simulate_transaction_update | Simulate updates |

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLite with aiosqlite
- **API**: Plaid Python SDK
- **Config**: Pydantic Settings

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **State**: React Hooks

## Development

### Backend Development

```bash
# Run with auto-reload
uvicorn main:app --reload

# Run tests (when added)
pytest
```

### Frontend Development

```bash
cd frontend

# Dev server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Security Notes

- `.env` file is gitignored - never commit credentials
- Database files are excluded from git
- Use HTTPS in production
- Implement webhook verification for production
- Plaid credentials should be stored securely

## Database Schema

**items** - Connected bank accounts
- `id`, `access_token`, `institution`, `cursor`, `created_at`

**transactions** - Bank transactions
- `id`, `item_id`, `plaid_txn_id`, `pending`, `amount`, `merchant_name`, etc.

**tips** - Tip records and overcharge status
- `id`, `pending_txn_id`, `expected_tip_amount`, `expected_total`, `actual_total`, `is_overcharged`, etc.

## Troubleshooting

**Backend won't start**
- Check `.env` file exists with valid Plaid credentials
- Ensure virtual environment is activated
- Verify all dependencies installed: `pip install -r requirements.txt`

**Frontend won't start**
- Run `npm install` in frontend directory
- Check Node.js version (16+)
- Clear `node_modules` and reinstall if needed

**Plaid Link not loading**
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify Plaid credentials in `.env`

## License

MIT License - feel free to use this project!

## Contributing

Contributions welcome! Please open an issue or PR.
