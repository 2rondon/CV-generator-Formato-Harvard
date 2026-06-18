from database.connection import get_connection

class CVController:
    @staticmethod
    def get_profile(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT full_name, email, phone, location, linkedin, github FROM profile WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"full_name": row[0] or "", "email": row[1] or "", "phone": row[2] or "", "location": row[3] or "", "linkedin": row[4] or "", "github": row[5] or ""}
        return {}

    @staticmethod
    def save_profile(user_id, data):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE profile SET full_name=?, email=?, phone=?, location=?, linkedin=?, github=? WHERE user_id=?
        ''', (data['full_name'], data['email'], data['phone'], data['location'], data['linkedin'], data['github'], user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_items(table, user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE user_id = ?", (user_id,))
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return results

    @staticmethod
    def add_item(table, data):
        conn = get_connection()
        cursor = conn.cursor()
        keys = ", ".join(data.keys())
        question_marks = ", ".join(["?"] * len(data))
        cursor.execute(f"INSERT INTO {table} ({keys}) VALUES ({question_marks})", list(data.values()))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_item(table, item_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table} WHERE id = ?", (item_id,))
        conn.commit()
        conn.close()