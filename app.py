from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# In-memory database (list)
expenses = []

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Get all expenses OR add a new expense
@app.route("/expenses", methods=["GET", "POST"])
def handle_expenses():
    if request.method == "POST":
        data = request.json
        expense = {
            "id": len(expenses) + 1,
            "amount": data["amount"],
            "category": data["category"],
            "date": data["date"],
            "note": data.get("note", "")
        }
        expenses.append(expense)
        return jsonify(expense), 201
    return jsonify(expenses)

# Update expense by ID
@app.route("/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    data = request.json
    expense = next((exp for exp in expenses if exp["id"] == expense_id), None)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    expense["amount"] = data.get("amount", expense["amount"])
    expense["category"] = data.get("category", expense["category"])
    expense["date"] = data.get("date", expense["date"])
    expense["note"] = data.get("note", expense["note"])

    return jsonify(expense)


# Get single expense by ID
@app.route("/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    expense = next((exp for exp in expenses if exp["id"] == expense_id), None)
    if expense:
        return jsonify(expense)
    return jsonify({"error": "Expense not found"}), 404

# Delete expense by ID
@app.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    global expenses
    expenses = [exp for exp in expenses if exp["id"] != expense_id]
    return jsonify({"message": "Expense deleted"})


if __name__ == "__main__":
    app.run(debug=True)
