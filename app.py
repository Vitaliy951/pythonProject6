from flask import Flask, render_template, request, jsonify
from src.main import load_json, load_csv, load_excel  # Импортируем необходимые функции
from src.views import events_view
from src.services import analyze_cashback_categories, investment_bank
from src.reports import spending_by_category

app = Flask(__name__)

@app.route('/')
def home():
    """Главная страница с меню."""
    return render_template('home.html')


@app.route('/main', methods=['POST'])
def main():
    """Пример маршрута для главной страницы."""
    return render_template('main.html')

@app.route('/events', methods=['POST'])
def events():
    """Обработка событий через API."""
    return events_view(request)

@app.route('/services/cashback_analysis', methods=['POST'])
def cashback_analysis():
    """Анализ выгодных категорий повышенного кешбэка."""
    data = request.json
    if not data or 'year' not in data or 'month' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    year = data['year']
    month = data['month']
    transactions = data.get('transactions', [])
    result = analyze_cashback_categories(transactions, year, month)
    return jsonify(result)

@app.route('/services/investment_bank', methods=['POST'])
def investment_service():
    """Расчет суммы для инвесткопилки."""
    data = request.json
    if not data or 'month' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    month = data['month']
    transactions = data.get('transactions', [])
    limit = data.get('limit', 100)
    result = investment_bank(month, transactions, limit)
    return jsonify({'total_investment': result})

@app.route('/services/simple_search', methods=['POST'])
def simple_search():
    """Простой поиск."""
    data = request.json
    if not data or 'query' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    query = data['query']
    # Логика поиска (пример)
    return jsonify({'result': f'search result for {query}'})

@app.route('/services/phone_search', methods=['POST'])
def phone_search():
    """Поиск по номеру телефона."""
    data = request.json
    if not data or 'phone_number' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    phone_number = data['phone_number']
    # Логика поиска по номеру телефона (пример)
    return jsonify({'result': f'search result for phone number {phone_number}'})

@app.route('/services/person_transfer_search', methods=['POST'])
def person_transfer_search():
    """Поиск по переводам между людьми."""
    data = request.json
    if not data or 'person_id' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    person_id = data['person_id']
    # Логика поиска по переводам (пример)
    return jsonify({'result': f'transfer search result for person {person_id}'})

@app.route('/reports/spending_by_category', methods=['POST'])
def spending_by_category_report():
    """Отчет по тратам по категории."""
    data = request.json
    if not data or 'transactions' not in data or 'category' not in data or 'date' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    transactions = data['transactions']
    category = data['category']
    date = data['date']
    result = spending_by_category(transactions, category, date)
    return jsonify(result)

@app.route('/reports/spending_by_weekday', methods=['POST'])
def spending_by_weekday_report():
    """Отчет по тратам по дням недели."""
    data = request.json
    transactions = data.get('transactions', [])
    # Логика формирования отчета (пример)
    return jsonify({'report': 'spending by weekday report', 'transactions': transactions})

@app.route('/reports/spending_by_workday', methods=['POST'])
def spending_by_workday_report():
    """Отчет по тратам по рабочим дням."""
    data = request.json
    transactions = data.get('transactions', [])
    # Логика формирования отчета (пример)
    return jsonify({'report': 'spending by workday report', 'transactions': transactions})

@app.route('/load_json', methods=['GET'])
def load_json_route():
    try:
        data = load_json('data/operations.json')
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/load_csv', methods=['GET'])
def load_csv_route():
    try:
        data = load_csv('data/transactions.csv')
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/load_excel', methods=['GET'])
def load_excel_route():
    try:
        data = load_excel('data/operations.xlsx')
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
