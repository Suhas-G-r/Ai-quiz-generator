import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.abspath(os.getcwd()), "quiz_database.db")

def get_db_connection():
    """Establishes and returns a connection to the SQLite database."""
    try:
        return sqlite3.connect(DATABASE_PATH)
    except sqlite3.Error as error:
        print(f"Database connection error: {error}")
        return None

def migrate_database():
    """Initializes the database schema and performs necessary migrations."""
    conn = get_db_connection()
    if not conn:
        return
        
    try:
        with conn:
            cursor = conn.cursor()
            
            # Create the main quizzes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quiz_table (
                    topic TEXT,
                    question TEXT,
                    option_a TEXT,
                    option_b TEXT,
                    option_c TEXT,
                    option_d TEXT,
                    correct_answer CHAR(1),
                    difficulty TEXT DEFAULT 'Medium',
                    explanation TEXT DEFAULT ''
                )
            """)
            
            # Create the quiz attempts history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attempts_table (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    topic TEXT,
                    score INTEGER,
                    total_questions INTEGER,
                    percentage REAL
                )
            """)
            
            # Verify and migrate legacy schemas if they exist without newer columns
            cursor.execute("PRAGMA table_info(quiz_table)")
            existing_columns = [column[1] for column in cursor.fetchall()]
            
            if 'difficulty' not in existing_columns:
                cursor.execute("ALTER TABLE quiz_table ADD COLUMN difficulty TEXT DEFAULT 'Medium'")
                print("Migration: Added 'difficulty' column to quiz_table.")
                
            if 'explanation' not in existing_columns:
                cursor.execute("ALTER TABLE quiz_table ADD COLUMN explanation TEXT DEFAULT ''")
                print("Migration: Added 'explanation' column to quiz_table.")
    except Exception as error:
        print(f"Error during schema migration: {error}")
    finally:
        conn.close()

# Run migrations when database module is imported
migrate_database()

def create_quiz(topic, quiz_questions, difficulty="Medium"):
    """Inserts a list of generated quiz questions into the database."""
    conn = get_db_connection()
    if not conn:
        return
        
    try:
        with conn:
            cursor = conn.cursor()
            for q in quiz_questions:
                explanation = q.get('explanation', '')
                cursor.execute("""
                    INSERT INTO quiz_table (topic, question, option_a, option_b, option_c, option_d, correct_answer, difficulty, explanation)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (topic, q['q'], q['A'], q['B'], q['C'], q['D'], q['correct'], difficulty, explanation))
    except sqlite3.Error as error:
        print(f"Failed to save quiz: {error}")
    finally:
        conn.close()

def get_quiz(topic):
    """Retrieves all questions associated with a given topic from the database."""
    conn = get_db_connection()
    if not conn:
        return []
        
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT question, option_a, option_b, option_c, option_d, correct_answer, difficulty, explanation
            FROM quiz_table
            WHERE topic = ?
        """, (topic,))
        rows = cursor.fetchall()
        
        quiz_data = []
        for row in rows:
            # Handle potential nulls safely
            diff = row[6] if len(row) > 6 and row[6] is not None else "Medium"
            exp = row[7] if len(row) > 7 and row[7] is not None else ""
            quiz_data.append({
                'question': row[0],
                'option_a': row[1],
                'option_b': row[2],
                'option_c': row[3],
                'option_d': row[4],
                'correct_answer': row[5],
                'difficulty': diff,
                'explanation': exp
            })
        return quiz_data
    except sqlite3.Error as error:
        print(f"Failed to fetch quiz: {error}")
        return []
    finally:
        conn.close()

def delete_quiz(topic):
    """Deletes a quiz and all its questions from the database."""
    conn = get_db_connection()
    if not conn:
        return
        
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM quiz_table WHERE topic = ?", (topic,))
    except sqlite3.Error as error:
        print(f"Failed to delete quiz: {error}")
    finally:
        conn.close()

def get_topics():
    """Retrieves all distinct quiz topics available in the database."""
    conn = get_db_connection()
    if not conn:
        return []
        
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT topic FROM quiz_table")
        topics = cursor.fetchall()
        return [t[0] for t in topics]
    except sqlite3.Error as error:
        print(f"Failed to fetch topics: {error}")
        return []
    finally:
        conn.close()

def save_attempt(topic, score, total_questions, percentage):
    """Saves a user's quiz attempt statistics to the history log."""
    conn = get_db_connection()
    if not conn:
        return
        
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attempts_table (topic, score, total_questions, percentage)
                VALUES (?, ?, ?, ?)
            """, (topic, score, total_questions, percentage))
    except sqlite3.Error as error:
        print(f"Failed to save score history: {error}")
    finally:
        conn.close()

def get_attempts():
    """Fetches all quiz attempts in reverse chronological order."""
    conn = get_db_connection()
    if not conn:
        return []
        
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, date, topic, score, total_questions, percentage
            FROM attempts_table
            ORDER BY date DESC
        """)
        rows = cursor.fetchall()
        
        attempts = []
        for r in rows:
            attempts.append({
                'id': r[0],
                'date': r[1],
                'topic': r[2],
                'score': r[3],
                'total_questions': r[4],
                'percentage': r[5]
            })
        return attempts
    except sqlite3.Error as error:
        print(f"Failed to retrieve score history: {error}")
        return []
    finally:
        conn.close()