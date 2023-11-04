from flask import Flask, render_template, session, redirect, url_for, request
from flask_session import Session
import json

app = Flask(__name__)

# Configure the Flask app to use Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'  # You can choose other options as well
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = False  # Optional: Use a signer to protect session data
app.config['SESSION_KEY_PREFIX'] = 'my_session_'  # Change this to a unique prefix
Session(app)

# Load the JSON data from the questions.json file
with open('questions.json', 'r') as json_file:
    questions_data = json.load(json_file)

@app.route('/')
def index():
    return render_template('index.html')

# Define a route for /quiz
@app.route('/quiz')
def quiz():
    
   
  # Initialize or get the current question index from session or elsewhere
    current_question_index = session.get('current_question_index', 0)
    user_responses = session.get('user_responses', [])
    
    if current_question_index == 0:
        session['current_question_index'] = 0
        user_responses.clear()
        session['user_responses'] = user_responses
        print('Cleared list')

    if current_question_index < len(questions_data['questions']):
        current_question = questions_data['questions'][current_question_index]
        return render_template('quiz.html',question =current_question, next_index=current_question_index + 1,user_responses=user_responses)
    else:
        return render_template('quizcompleted.html',question=0,next_index=0,user_responses = user_responses)
    
    
@app.route('/question/<int:question_index>', methods=['GET', 'POST'])
def get_question(question_index):
    

      
    user_responses = session.get('user_responses', [])
    
    if question_index == 0:
        session['current_question_index'] = 0
        user_responses.clear()
        print('Cleared list')
        
    if question_index >= 0 and question_index < len(questions_data['questions']):
        if request.method == 'POST':
            # Process the user's response here if needed
            user_response = request.form['answer']  # Get the selected radio button value
            user_responses.append(user_response)  # Store the user's response

            # Update the current question index in the session
            session['current_question_index'] = question_index
            session['user_responses'] = user_responses
            
            # Redirect to the next question
            return redirect(url_for('get_question',question_index=question_index))
        else:
            current_question = questions_data['questions'][question_index]
            return render_template('quiz.html', question=current_question, next_index=question_index + 1,user_responses=user_responses)
    else:
        current_question_index = session.get('current_question_index', 0)
        return render_template('quizcompleted.html',question=0,next_index=0,user_responses = user_responses)

    
if __name__ == '__main__':
    app.run(debug=True)