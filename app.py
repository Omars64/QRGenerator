from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)

# In-memory storage for players and transactions
players = {}
transactions = []

# Default starting money in Monopoly
DEFAULT_STARTING_MONEY = 1500

def save_data():
    """Save players and transactions to files"""
    with open('players.json', 'w') as f:
        json.dump(players, f)
    with open('transactions.json', 'w') as f:
        json.dump(transactions, f)

def load_data():
    """Load players and transactions from files"""
    global players, transactions
    try:
        if os.path.exists('players.json'):
            with open('players.json', 'r') as f:
                players = json.load(f)
        if os.path.exists('transactions.json'):
            with open('transactions.json', 'r') as f:
                transactions = json.load(f)
    except:
        players = {}
        transactions = []

@app.route('/')
def index():
    load_data()
    return render_template('index.html', players=players, transactions=transactions[-10:])

@app.route('/add_player', methods=['POST'])
def add_player():
    name = request.form.get('name', '').strip()
    if name and name not in players:
        players[name] = DEFAULT_STARTING_MONEY
        transactions.append({
            'id': len(transactions),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'Player Added',
            'from_player': 'Bank',
            'to_player': name,
            'amount': DEFAULT_STARTING_MONEY,
            'description': f'Starting money for {name}'
        })
        save_data()
    return redirect(url_for('index'))

@app.route('/remove_player', methods=['POST'])
def remove_player():
    name = request.form.get('name', '').strip()
    if name in players:
        final_balance = players[name]
        del players[name]
        transactions.append({
            'id': len(transactions),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'Player Removed',
            'from_player': name,
            'to_player': 'Bank',
            'amount': final_balance,
            'description': f'{name} removed from game with ${final_balance}'
        })
        save_data()
    return redirect(url_for('index'))

@app.route('/transfer', methods=['POST'])
def transfer():
    from_player = request.form.get('from_player', '').strip()
    to_player = request.form.get('to_player', '').strip()
    amount = request.form.get('amount', '0')
    description = request.form.get('description', '').strip()
    
    try:
        amount = int(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        if from_player not in players or to_player not in players:
            raise ValueError("Invalid players")
        
        if from_player == to_player:
            raise ValueError("Cannot transfer to same player")
        
        if players[from_player] < amount:
            raise ValueError("Insufficient funds")
        
        # Perform transfer
        players[from_player] -= amount
        players[to_player] += amount
        
        transactions.append({
            'id': len(transactions),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'Transfer',
            'from_player': from_player,
            'to_player': to_player,
            'amount': amount,
            'description': description or f'Transfer from {from_player} to {to_player}'
        })
        save_data()
        
    except ValueError as e:
        # In a real app, you'd handle this error properly
        pass
    
    return redirect(url_for('index'))

@app.route('/bank_payment', methods=['POST'])
def bank_payment():
    player = request.form.get('player', '').strip()
    amount = request.form.get('amount', '0')
    description = request.form.get('description', '').strip()
    transaction_type = request.form.get('transaction_type', 'receive')
    
    try:
        amount = int(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        if player not in players:
            raise ValueError("Invalid player")
        
        if transaction_type == 'pay' and players[player] < amount:
            raise ValueError("Insufficient funds")
        
        # Perform bank transaction
        if transaction_type == 'receive':
            players[player] += amount
            from_player = 'Bank'
            to_player = player
        else:  # pay
            players[player] -= amount
            from_player = player
            to_player = 'Bank'
        
        transactions.append({
            'id': len(transactions),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'Bank Transaction',
            'from_player': from_player,
            'to_player': to_player,
            'amount': amount,
            'description': description or f'{player} {transaction_type} ${amount}'
        })
        save_data()
        
    except ValueError as e:
        # In a real app, you'd handle this error properly
        pass
    
    return redirect(url_for('index'))

@app.route('/get_players')
def get_players():
    load_data()
    return jsonify(list(players.keys()))

@app.route('/reset_game', methods=['POST'])
def reset_game():
    global players, transactions
    players = {}
    transactions = []
    save_data()
    return redirect(url_for('index'))

if __name__ == '__main__':
    load_data()
    app.run(debug=True, host='0.0.0.0', port=5000)
