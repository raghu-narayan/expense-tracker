from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os

# Initialize Flask app with correct paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)
CORS(app)

# Use /tmp for SQLite in serverless environment
DATABASE = '/tmp/expenses.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            family_member TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    category = request.args.get('category')
    family_member = request.args.get('family_member')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    conn = get_db()
    cursor = conn.cursor()

    query = 'SELECT * FROM expenses WHERE 1=1'
    params = []

    if category:
        query += ' AND category = ?'
        params.append(category)
    if family_member:
        query += ' AND family_member = ?'
        params.append(family_member)
    if start_date:
        query += ' AND date >= ?'
        params.append(start_date)
    if end_date:
        query += ' AND date <= ?'
        params.append(end_date)

    query += ' ORDER BY date DESC, created_at DESC'

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])

@app.route('/api/expenses', methods=['POST'])
def create_expense():
    data = request.get_json()

    if not all([data.get('amount'), data.get('category'), data.get('date'), data.get('family_member')]):
        return jsonify({'error': 'Amount, category, date, and family_member are required'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (amount, category, description, date, family_member)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['amount'], data['category'], data.get('description', ''), data['date'], data['family_member']))
    conn.commit()
    expense_id = cursor.lastrowid
    conn.close()

    return jsonify({'id': expense_id, 'message': 'Expense created successfully'})

@app.route('/api/expenses/<int:id>', methods=['PUT'])
def update_expense(id):
    data = request.get_json()

    if not all([data.get('amount'), data.get('category'), data.get('date'), data.get('family_member')]):
        return jsonify({'error': 'Amount, category, date, and family_member are required'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE expenses
        SET amount = ?, category = ?, description = ?, date = ?, family_member = ?
        WHERE id = ?
    ''', (data['amount'], data['category'], data.get('description', ''), data['date'], data['family_member'], id))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Expense not found'}), 404

    conn.close()
    return jsonify({'message': 'Expense updated successfully'})

@app.route('/api/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Expense not found'}), 404

    conn.close()
    return jsonify({'message': 'Expense deleted successfully'})

@app.route('/api/summary', methods=['GET'])
def get_summary():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    conn = get_db()
    cursor = conn.cursor()

    date_filter = ''
    params = []

    if start_date and end_date:
        date_filter = 'WHERE date >= ? AND date <= ?'
        params = [start_date, end_date]
    elif start_date:
        date_filter = 'WHERE date >= ?'
        params = [start_date]
    elif end_date:
        date_filter = 'WHERE date <= ?'
        params = [end_date]

    cursor.execute(f'SELECT COALESCE(SUM(amount), 0) as total FROM expenses {date_filter}', params)
    total = cursor.fetchone()['total']

    cursor.execute(f'''
        SELECT category, COALESCE(SUM(amount), 0) as total, COUNT(*) as count
        FROM expenses {date_filter}
        GROUP BY category
        ORDER BY total DESC
    ''', params)
    by_category = [dict(row) for row in cursor.fetchall()]

    cursor.execute(f'''
        SELECT family_member, COALESCE(SUM(amount), 0) as total, COUNT(*) as count
        FROM expenses {date_filter}
        GROUP BY family_member
        ORDER BY total DESC
    ''', params)
    by_member = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify({
        'total': total,
        'byCategory': by_category,
        'byFamilyMember': by_member
    })

@app.route('/api/filters', methods=['GET'])
def get_filters():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT DISTINCT category FROM expenses ORDER BY category')
    categories = [row['category'] for row in cursor.fetchall()]

    cursor.execute('SELECT DISTINCT family_member FROM expenses ORDER BY family_member')
    members = [row['family_member'] for row in cursor.fetchall()]

    conn.close()

    return jsonify({
        'categories': categories,
        'familyMembers': members
    })