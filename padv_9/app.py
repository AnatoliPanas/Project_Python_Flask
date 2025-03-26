from padv_9.app_runner import create_app
from padv_9.models.questions import Question, Statistic
from padv_9.models.answers import Answer


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
