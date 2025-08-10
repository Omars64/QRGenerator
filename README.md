# Monopoly Banking System

A modern web-based banking system for Monopoly games that supports multiple players with convenient dropdown selection for all transactions.

## Features

- **Player Management**: Add and remove players with automatic starting money ($1,500)
- **Player-to-Player Transfers**: Transfer money between players with dropdown selection
- **Bank Transactions**: Handle payments to/from the bank (salary, taxes, etc.)
- **Transaction History**: Track all financial activities with timestamps
- **Modern UI**: Clean, responsive interface with Monopoly-themed styling
- **Data Persistence**: Game state is saved automatically
- **Input Validation**: Prevents invalid transactions and insufficient funds

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Usage

### Adding Players
1. Enter a player name in the "Add New Player" field
2. Click "Add Player" - they will automatically receive $1,500 starting money

### Transferring Money
1. Select the sender from the "From Player" dropdown (shows current balance)
2. Select the recipient from the "To Player" dropdown
3. Enter the amount and optional description
4. Click "Transfer Money"

### Bank Transactions
1. Select a player from the dropdown
2. Choose "Receive from Bank" or "Pay to Bank"
3. Enter the amount and optional description (e.g., "GO", "Tax", "Salary")
4. Click "Process Bank Transaction"

### Managing the Game
- View all player balances in the "Current Players" section
- Monitor recent transactions in the "Transaction History"
- Remove players using the dropdown in "Player Management"
- Reset the entire game using "Reset Game" (with confirmation)

## Technical Details

- Built with Flask (Python web framework)
- Responsive design works on desktop and mobile
- Data is persisted in JSON files (`players.json` and `transactions.json`)
- Real-time balance updates and transaction logging
- Input validation prevents common errors

## Game Rules Integration

The system follows standard Monopoly banking rules:
- Starting money: $1,500 per player
- All transactions are tracked with timestamps
- Prevents transfers with insufficient funds
- Supports common Monopoly transactions (rent, salary, taxes, etc.)

Enjoy your Monopoly game with hassle-free digital banking!