from flask import Flask, render_template, request, redirect, url_for, session
import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'

PASSWORD = "1234"  # simple password for login

# Store projects and transactions
data = {
    'projects': [],
    'transactions': []
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="رمز اشتباه است!")
    return render_template('login.html')

@app.before_request
def require_login():
    if request.endpoint not in ['login', 'static'] and not session.get('logged_in'):
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():
    project_filter = request.args.get('project')
    filtered_transactions = data['transactions']

    if project_filter and project_filter != 'All':
        filtered_transactions = [t for t in data['transactions'] if t['project'] == project_filter]

    balance = sum(t['amount'] if t['type'] == 'income' else -t['amount'] for t in filtered_transactions)
    return render_template('index.html', balance=balance, transactions=filtered_transactions, projects=data['projects'], selected_project=project_filter or 'All')

@app.route('/add_project', methods=['POST'])
def add_project():
    new_project = request.form.get('project_name')
    if new_project and new_project not in data['projects']:
        data['projects'].append(new_project)
    return redirect(url_for('index'))

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    description = request.form.get('description')
    amount = float(request.form.get('amount'))
    date = request.form.get('date')
    trans_type = request.form.get('type')
    project = request.form.get('project')

    transaction = {
        'description': description,
        'amount': amount,
        'date': date,
        'type': trans_type,
        'project': project
    }
    data['transactions'].append(transaction)
    return redirect(url_for('index'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

