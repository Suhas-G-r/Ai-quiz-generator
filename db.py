import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as error:
        print(f"Database connection error: {error}")
        return None

def migrate_database():
    """Initializes the database schema."""
    conn = get_db_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
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
                explanation TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attempts_table (
                id SERIAL PRIMARY KEY,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                topic TEXT,
                score INTEGER,
                total_questions INTEGER,
                percentage REAL
            )
        """)
        cursor.execute("""
            ALTER TABLE quiz_table 
            ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        """)
        conn.commit()
    except Exception as error:
        print(f"Error during schema migration: {error}")
    finally:
        conn.close()

migrate_database()

def create_quiz(topic, quiz_questions, difficulty="Medium"):
    """Inserts a list of generated quiz questions into the database."""
    conn = get_db_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        for q in quiz_questions:
            explanation = q.get('explanation', '')
            cursor.execute("""
                INSERT INTO quiz_table (topic, question, option_a, option_b, option_c, option_d, correct_answer, difficulty, explanation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (topic, q['q'], q['A'], q['B'], q['C'], q['D'], q['correct'], difficulty, explanation))
        conn.commit()
    except Exception as error:
        print(f"Failed to save quiz: {error}")
    finally:
        conn.close()

def get_quiz(topic):
    """Retrieves all questions for a given topic."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT question, option_a, option_b, option_c, option_d, correct_answer, difficulty, explanation
            FROM quiz_table WHERE topic = %s
        """, (topic,))
        rows = cursor.fetchall()
        quiz_data = []
        for row in rows:
            quiz_data.append({
                'question': row[0],
                'option_a': row[1],
                'option_b': row[2],
                'option_c': row[3],
                'option_d': row[4],
                'correct_answer': row[5],
                'difficulty': row[6] if row[6] else "Medium",
                'explanation': row[7] if row[7] else ""
            })
        return quiz_data
    except Exception as error:
        print(f"Failed to fetch quiz: {error}")
        return []
    finally:
        conn.close()

def delete_quiz(topic):
    """Deletes a quiz and its attempt history from the database."""
    conn = get_db_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM quiz_table WHERE topic = %s", (topic,))
        cursor.execute("DELETE FROM attempts_table WHERE topic = %s", (topic,))
        conn.commit()
    except Exception as error:
        print(f"Failed to delete quiz: {error}")
    finally:
        conn.close()

def get_topics():
    """Retrieves all distinct quiz topics in order of creation."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT topic FROM quiz_table
            GROUP BY topic
            ORDER BY MIN(created_at) ASC
        """)
        topics = cursor.fetchall()
        return [t[0] for t in topics]
    except Exception as error:
        print(f"Failed to fetch topics: {error}")
        return []
    finally:
        conn.close()

def save_attempt(topic, score, total_questions, percentage):
    """Saves a quiz attempt to history."""
    conn = get_db_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO attempts_table (topic, score, total_questions, percentage)
            VALUES (%s, %s, %s, %s)
        """, (topic, score, total_questions, percentage))
        conn.commit()
    except Exception as error:
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
            FROM attempts_table ORDER BY date DESC
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
    except Exception as error:
        print(f"Failed to retrieve score history: {error}")
        return []
    finally:
        conn.close()