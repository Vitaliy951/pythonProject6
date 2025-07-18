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


@app.route('/main', methods=['GET'])
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
    year = data.get('year')
    month = data.get('month')
    transactions = data.get('transactions', [])
    result = analyze_cashback_categories(transactions, year, month)
    return jsonify(result)


@app.route('/services/investment_bank', methods=['POST'])
def investment_service():
    """Расчет суммы для инвесткопилки."""
    data = request.json
    month = data.get('month')
    transactions = data.get('transactions', [])
    limit = data.get('limit', 100)
    result = investment_bank(month, transactions, limit)
    return jsonify({'total_investment': result})


@app.route('/services/simple_search', methods=['POST'])
def simple_search():
    """Простой поиск."""
    data = request.json
    query = data.get('query')
    # Логика поиска (пример)
    return jsonify({'result': 'search result for {}'.format(query)})


@app.route('/services/phone_search', methods=['POST'])
def phone_search():
    """Поиск по номеру телефона."""
    data = request.json
    phone_number = data.get('phone_number')
    # Логика поиска по номеру телефона (пример)
    return jsonify({'result': 'search result for phone number {}'.format(phone_number)})


@app.route('/services/person_transfer_search', methods=['POST'])
def person_transfer_search():
    """Поиск по переводам между людьми."""
    data = request.json
    person_id = data.get('person_id')
    # Логика поиска по переводам (пример)
    return jsonify({'result': 'transfer search result for person {}'.format(person_id)})


@app.route('/reports/spending_by_category', methods=['POST'])
def spending_by_category_report():
    """Отчет по тратам по категории."""
    data = request.json
    transactions = data.get('transactions', [])
    category = data.get('category')
    date = data.get('date')
    result = spending_by_category(transactions, category, date)
    return jsonify(result)


@app.route('/reports/spending_by_weekday', methods=['POST'])
def spending_by_weekday_report():
    """Отчет по тратам по дням недели."""
    data = request.json
    transactions = data.get('transactions', [])
    # Логика формирования отчета (пример)
    return jsonify({'report': 'spending by weekday report'})


@app.route('/reports/spending_by_workday', methods=['POST'])
def spending_by_workday_report():
    """Отчет по тратам по рабочим дням."""
    data = request.json
    transactions = data.get('transactions', [])
    # Логика формирования отчета (пример)
    return jsonify({'report': 'spending by workday report'})


@app.route('/load_json', methods=['GET'])
def load_json_route():
    try:
        data = load_json('data/operations.json')
        return jsonify(data), 200
    except Exception as e:
        return str(e), 500


@app.route('/load_csv', methods=['GET'])
def load_csv_route():
    try:
        data = load_csv('data/transactions.csv')
        return jsonify(data), 200
    except Exception as e:
        return str(e), 500


@app.route('/load_excel', methods=['GET'])
def load_excel_route():
    try:
        data = load_excel('data/operations.xlsx')
        return jsonify(data), 200
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True)
