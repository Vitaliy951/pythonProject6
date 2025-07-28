from flask import Flask, request, jsonify
from src.utils import read_json_file
from src.generators import filter_by_currency, transaction_descriptions
from src.processing import filter_by_state, sort_by_date
from src.widget import mask_account_card

app = Flask(__name__)


@app.route("/transactions", methods=["POST"])
def process_transactions():
    data = request.json
    file_path = data.get("file_path")
    currency_code = data.get("currency_code")
    state = data.get("state")
    sort_order = data.get("sort_order")

    transactions = read_json_file(file_path)
    if not transactions:
        return jsonify({"error": "Не удалось загрузить транзакции."}), 400

    filtered_transactions = filter_by_currency(transactions, currency_code)
    filtered_by_state = filter_by_state(filtered_transactions, state)

    ascending = sort_order == "возрастание"
    sorted_transactions = sort_by_date(filtered_by_state, ascending)

    descriptions = list(transaction_descriptions(sorted_transactions))
    masked_info = [
        mask_account_card(f"{t.get('account_type', 'счет')} {t.get('account_number', '')}")
        for t in sorted_transactions
    ]

    return jsonify({"descriptions": descriptions, "masked_info": masked_info})


if __name__ == "__main__":
    app.run(debug=True)
