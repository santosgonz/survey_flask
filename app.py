from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

##to append the answers later
responses = []

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/start_session", methods=["POST"])
def start_session():
    session["responses"] = []
    print(session)
    return redirect("/questions/0")


@app.route("/start")
def start_page():
    title = survey.title
    instructions = survey.instructions
    return render_template("start.html", title=title, instructions=instructions)

@app.route("/questions/<int:id>", methods=["GET", "POST"])
##Why the am i skipping page?//
def question_page(id):
    try:
        question = survey.questions[id]

        if request.method == "POST":
            print(session)
            answers = session.get("answers", [])
            new_answer = request.form["answer"]
            answers.append(new_answer)
            session["answers"] = answers
            # print (session["answers"])
            # print(answers)
            # print(new_answer)
        #####TEST######
            # session["responses"] = request.form["answer"]
        #####TESTING SESSION####
            # answer_selected = request.form["answer"]
            # responses.append(answer_selected)

            new_page_id = id + 1

            if new_page_id < len(survey.questions):
                return redirect(f"/questions/{new_page_id}")
            return redirect("/thank_you_page")

        if id >= len(survey.questions):
            flash("You shouldn't be here!")
            return redirect("/start")
        print (session["responses"])
        
        return render_template("questions.html", question=question, id=id)
    
    except IndexError as e:
        print(e)
        flash("invalid index")
        return redirect("/start")


@app.route("/thank_you_page")
def thank_you():
    return render_template("thank_you.html", responses=responses)