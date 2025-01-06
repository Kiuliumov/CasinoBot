import sqlite3

class DB:
    CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        money INT DEFAULT 250
    );
    """

    def __init__(self):
        self.con = sqlite3.connect('casino.db')
        self.cur = self.con.cursor()
        self.cur.execute(self.CREATE_TABLE)
        self.con.commit()

    def new_user(self, initial_money=250):
        self.cur.execute("INSERT INTO users (money) VALUES (?)", (initial_money,))
        self.con.commit()
        return self.cur.lastrowid

    def take_money(self, user_id, amount):
        self.cur.execute("SELECT money FROM users WHERE id = ?", (user_id,))
        result = self.cur.fetchone()
        if result:
            current_money = result[0]
            if current_money >= amount:
                new_money = current_money - amount
                self.cur.execute("UPDATE users SET money = ? WHERE id = ?", (new_money, user_id))
                self.con.commit()
                return True
            else:
                print("Insufficient funds!")
                return False
        else:
            print("User not found!")
            return False

    def give_money(self, user_id, amount):
        self.cur.execute("SELECT money FROM users WHERE id = ?", (user_id,))
        result = self.cur.fetchone()
        if result:
            current_money = result[0]
            new_money = current_money + amount
            self.cur.execute("UPDATE users SET money = ? WHERE id = ?", (new_money, user_id))
            self.con.commit()
            return True
        else:
            print("User not found!")
            return False

    def get_balance(self, user_id):
        self.cur.execute("SELECT money FROM users WHERE id = ?", (user_id,))
        result = self.cur.fetchone()
        return result[0] if result else None


    def check_if_user_is_registered(self, user_id):
           self.cur.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))
        result = self.cur.fetchone()
        return result is not None
