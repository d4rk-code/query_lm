from flask import Flask, render_template, request, jsonify
from db.execute import execute
from AI.summarizer import summarize 
from AI.query_gen import query_generator
from AI.memory import history as context

app = Flask(__name__)

@app.route('/')
def welcome():
    return "HOMEPAGE"

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.form.get("query")

        try:
            query = query_generator(user_input)
            print("THE QUERY ASKED: \n", query)

            data = execute(query)
            print("Results of the query: \n", data)
           
            summarizer_result = summarize(data)
            
            if hasattr(summarizer_result, '__iter__') and not isinstance(summarizer_result, str):
                summarized = "".join(list(summarizer_result))
            else:
                summarized = summarizer_result
                
            print("Summarized llm result: \n", summarized)

            # creating a context
            context.append({
                "question": user_input,
                "sql": query,
                "response": summarized
            })

            return jsonify({
                "status": "success",
                "question": user_input,
                "response": summarized
            })

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"System error encountered: {str(e)}"
            }), 500

    return render_template("chat/chat.html", question=None, response=None)

@app.route('/history')
def history() -> str: 
    return render_template('history/history.html', title='History')

if __name__ == "__main__":
    app.run(debug=True)
