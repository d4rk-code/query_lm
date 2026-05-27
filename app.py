from flask import Flask, render_template, request
from db.execute import execute
from AI.summarizer import summarize 
from AI.query_gen import query_generator

#---- web app ----
app = Flask(__name__)

@app.route('/')
def welcome():
    return "HOMEPAGE"

@app.route("/chat", methods=["GET", "POST"])
def chat():

    response = None
    user_input = None

    if request.method == "POST":

        user_input = request.form.get("query")

        query = query_generator(user_input)
        print("THE QUERY ASKED: \n", query)

        data = execute(query)
        print("Results of the query: \n", data)
       
        summarized = summarize(data)
        print("Summarized llm result: \n", summarized)

        response = summarized

    return render_template(
        "chat/chat.html",
        question = user_input,
        response = response
    )


@app.route('/history')
def history() -> str: 
    return render_template('history/history.html', title='History')

if(__name__ == "__main__"):
    app.run(debug=True)
