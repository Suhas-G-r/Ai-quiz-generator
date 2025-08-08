from flask import Flask, render_template, request, redirect, url_for, session
import db
from main import generate_quiz

web_app = Flask(__name__)
web_app.secret_key = 'ai-quiz-bot-session-key-suhas-gr'

@web_app.route('/')
def home_page():
    """Renders the main splash homepage."""
    return render_template('home.html')

@web_app.route('/about')
def about():
    """Renders the details and developer bio page."""
    return render_template('about.html')

@web_app.route('/quizzes')
def quizzes():
    """Renders a list of all currently created/stored quizzes."""
    available_topics = db.get_topics()
    return render_template('quizzes.html', topics=available_topics)

@web_app.route('/quiz/<topic>', methods=['GET', 'POST'])
def quiz(topic):
    """Handles quiz-taking display and submissions."""
    quiz_questions = db.get_quiz(topic)
    
    if request.method == 'POST':
        user_responses = request.form.to_dict()
        session['answers'] = user_responses
        
        # Calculate scores to log attempt
        correct_count = 0
        total_q = len(quiz_questions)
        for i, q in enumerate(quiz_questions):
            correct_ans = q['correct_answer']
            user_ans = user_responses.get(f'question{i+1}')
            if user_ans == correct_ans:
                correct_count += 1
                
        accuracy = (correct_count / total_q) * 100 if total_q > 0 else 0
        
        # Record score log in database
        db.save_attempt(topic, correct_count, total_q, accuracy)
        
        return redirect(url_for('quiz_summary', topic=topic))
        
    if quiz_questions:
        return render_template('quiz.html', topic=topic, questions=quiz_questions)
    return redirect(url_for('quizzes'))

@web_app.route('/delete_quiz/<topic>')
def delete_quiz(topic):
    """Deletes a quiz and redirects to list page."""
    db.delete_quiz(topic)
    return redirect(url_for('quizzes'))

@web_app.route('/create_quiz/<topic>', methods=['POST'])
def create_quiz(topic):
    """Processes request forms to construct a new quiz using Gemini AI."""
    topic_name = request.form['new_topic'].strip()
    total_questions = int(request.form.get('num_questions', 10))
    difficulty_level = request.form.get('difficulty', 'Medium')
    
    # Generate structured JSON quiz data from AI
    generated_data = generate_quiz(topic_name, number_of_questions=total_questions, difficulty=difficulty_level)
    
    # Save the generated quiz to sqlite database
    db.create_quiz(topic_name, generated_data, difficulty_level)
    
    return redirect(url_for('quizzes'))

@web_app.route('/quiz_summary/<topic>')
def quiz_summary(topic):
    """Aggregates and displays score review and correct/incorrect choices."""
    questions_list = db.get_quiz(topic)
    user_responses = session.get('answers', {})
    
    correct_count = 0
    attempted_count = 0
    total_q = len(questions_list)
    
    for i, q in enumerate(questions_list):
        correct_ans = q['correct_answer']
        user_ans = user_responses.get(f'question{i+1}')
        if user_ans:
            attempted_count += 1
            if user_ans == correct_ans:
                correct_count += 1
                
    accuracy = (correct_count / total_q) * 100 if total_q > 0 else 0
    
    return render_template(
        'quiz_summary.html', 
        topic=topic, 
        questions=questions_list, 
        answers=user_responses, 
        correct_count=correct_count, 
        attempted_count=attempted_count, 
        total_questions=total_q, 
        percentage=round(accuracy, 1)
    )

@web_app.route('/dashboard')
def dashboard():
    """Renders score history, progress timeline, and analytical charts."""
    history_logs = db.get_attempts()
    
    total_runs = len(history_logs)
    avg_accuracy = 0
    record_score = 0
    favorite_topic = "N/A"
    
    if total_runs > 0:
        avg_accuracy = sum(run['percentage'] for run in history_logs) / total_runs
        record_score = max(run['percentage'] for run in history_logs)
        
        # Calculate favorite topic (highest average percentage)
        topic_points = {}
        topic_counts = {}
        for run in history_logs:
            t = run['topic']
            topic_points[t] = topic_points.get(t, 0) + run['percentage']
            topic_counts[t] = topic_counts.get(t, 0) + 1
            
        best_average = -1
        for t, points in topic_points.items():
            avg = points / topic_counts[t]
            if avg > best_average:
                best_average = avg
                favorite_topic = t
                
    # Format data logs for visual chart timeline (last 10 attempts in oldest-to-newest order)
    timeline_logs = list(reversed(history_logs[:10]))
    chart_labels = [log['topic'] for log in timeline_logs]
    chart_scores = [log['percentage'] for log in timeline_logs]
    
    return render_template(
        'dashboard.html',
        attempts=history_logs,
        total_quizzes=total_runs,
        avg_accuracy=round(avg_accuracy, 1),
        highest_score=round(record_score, 1),
        best_topic=favorite_topic,
        chart_labels=chart_labels,
        chart_data=chart_scores
    )

if __name__ == '__main__':
    web_app.run(debug=True)
