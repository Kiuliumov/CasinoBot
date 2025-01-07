import sqlite3

class DB:
    CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        money INT DEFAULT 250
    );
    """

    def __init__(self):
        self.con = sqlite3.connect('casino.db')
        self.cur = self.con.cursor()
        self.cur.execute(self.CREATE_TABLE)
        self.con.commit()

    def new_user(self, user_id, initial_money=250):
        self.cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if self.cur.fetchone() is None:
            self.cur.execute("INSERT INTO users (id, money) VALUES (?, ?)", (user_id, initial_money))
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
       self.cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
       result = self.cur.fetchone()
       return result is not None

    def get_five_players(self, page):
        offset = (page - 1) * 5

        self.cur.execute("SELECT * FROM users ORDER BY money DESC LIMIT 5 OFFSET ?", (offset,))
        result = self.cur.fetchall()
        return result

    def insert_user_data(self, data):
        self.cur.executemany('''
        INSERT INTO users (id, money) VALUES (?, ?)
        ''', data)
        self.con.commit()

    @property
    def db_length(self):
        self.cur.execute("SELECT COUNT(*) FROM users")
        result = self.cur.fetchone()
        return result[0]
