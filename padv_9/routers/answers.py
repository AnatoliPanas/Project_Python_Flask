from flask import Blueprint, request

answers_bp = Blueprint(name="answers", import_name=__name__)

@answers_bp.route(rule='', methods=["GET", "POST"])
def work_with_answers():
    if request.method == "GET":
        return "Получен список всех ответов."

    if request.method == "POST":
        return "Создание нового ответа."


@answers_bp.route('/<int:id>', methods=["GET"])
def retrieve_answers(id):
    return f"Ответ на запрос по id - {id}"
