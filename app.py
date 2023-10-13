from flask import Flask, request, render_template, redirect,flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey
app = Flask(__name__)
app.config['SECRET_KEY'] ="oh-so-secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



@app.route("/")
def home_page():
  survey_tittle =satisfaction_survey.title
  print(survey_tittle)
  survey_instructions =satisfaction_survey.instructions
  return render_template("homepage.html", survey_tittle=survey_tittle,survey_instructions=survey_instructions)


@app.route("/session_setter",methods=["POST"] )
def session_setter():
 survey_tittle =satisfaction_survey.title
 survey_instructions =satisfaction_survey.instructions
 session["responses"] = []
 print(f"session data for responses {session['responses']}")
 return redirect("/questions/0")



@app.route("/questions/<int:questionNum>")
def questions(questionNum):
  responses = session["responses"]
  print("In questions")
  print(f"number_of_responses:{len(responses)} ")
  print(f"responses:{responses} ")
  number_of_responses = len(responses)
  if number_of_responses == questionNum:
    survey_tittle =satisfaction_survey.title
    number_of_questions = len(satisfaction_survey.questions)
    if questionNum == number_of_questions:
      print(responses)
      return  render_template("thankyou.html")
    else:
      question = satisfaction_survey.questions[questionNum].question
      choices = satisfaction_survey.questions[questionNum].choices
      print(question)
      print(choices)
      return render_template("question.html", question=question,survey_tittle= survey_tittle,choices =choices,questionNum=questionNum)
  else:
    flash("trying to access an invalid question! Please follow the order of the survey", 'error')
    return redirect(f"/questions/{len(responses)}")
  

@app.route("/answer",methods=["POST"])
def answer():
  responses =session["responses"]
  response = request.form["response"]
  responses.append(response)
  session["responses"] = responses
  current_question =int(request.form["questionNum"])
  next_question =current_question +1
  print(f"current_question:  {current_question } next question:{next_question}" )
  print("Printing responses from session")
  print(responses)
  return redirect(f"/questions/{next_question}")


  
  