import mysql.connector
from config import CONFIG

DB_CONFIG = {
    'host': CONFIG['DB_HOST'],
    'user': CONFIG['DB_USER'],
    'password': CONFIG['DB_PASSWORD'],
    'database': CONFIG['DB_NAME']
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_user(vk_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM players WHERE vk_id = %s", (vk_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def add_click_to_user(vk_id, clicks, balance_increase):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE players SET clicks = clicks + %s, balance = balance + %s WHERE vk_id = %s",
        (clicks, balance_increase, vk_id)
    )
    conn.commit()
    cursor.close()
    conn.close()