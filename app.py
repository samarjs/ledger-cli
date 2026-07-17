from flask import Flask, render_template, request, redirect, url_for, flash
from ledger.models import Entry, Transaction
from ledger.engine import LedgerEngine
from ledger.storage import Storage
from ledger.reports import ReportGenerator

app = Flask(__name__)
app.secret_key = 'ledger-secret-key'

# Initialize engine
storage = Storage()
engine = LedgerEngine(storage)
reports = ReportGenerator(engine)

@app.route('/')
def index():
    transactions = engine.get_transactions()
    trial = reports.trial_balance()
    return render_template('index.html', transactions=transactions, trial=trial)

@app.route('/add', methods=['POST'])
def add_transaction():
    try:
        date = request.form['date']
        description = request.form['description']
        
        # Parse entries from form
        accounts = request.form.getlist('account[]')
        amounts = request.form.getlist('amount[]')
        types = request.form.getlist('type[]')
        
        entries = []
        for i in range(len(accounts)):
            if accounts[i] and amounts[i] and types[i]:
                entries.append(Entry(accounts[i], amounts[i], types[i]))
        
        if len(entries) < 2:
            flash('Need at least 2 entries', 'error')
            return redirect(url_for('index'))
        
        tx = engine.add_transaction(date, description, entries)
        flash(f'Transaction {tx.id} added successfully!', 'success')
        
    except Exception as e:
        flash(str(e), 'error')
    
    return redirect(url_for('index'))

@app.route('/delete/<tx_id>')
def delete_transaction(tx_id):
    if engine.delete_transaction(tx_id):
        flash(f'Transaction {tx_id} deleted', 'success')
    else:
        flash(f'Transaction {tx_id} not found', 'error')
    return redirect(url_for('index'))

@app.route('/ledger')
def view_ledger():
    ledger_report = reports.ledger()
    return render_template('ledger.html', ledger=ledger_report)

if __name__ == '__main__':
    app.run(debug=True)