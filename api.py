import db_config as db
import sqlite3

class DBApi():
    conn = sqlite3.connect(db.sqlite_db['database'])
    curs = conn.cursor()
    
    """ Function to add new user to database
        Arguments:
            name: Name of user to add
            phone_number: Phone number of user to add
    """
    def insert_user(self, name, phone_number):
        try:
            if name and phone_number:
                sql = "INSERT INTO "+ db.sqlite_db['table'] +"(name, phone_number) VALUES (?, ?)"
                args = (name, phone_number)
                self.curs.execute(sql, args)
                self.conn.commit()
                if self.conn.total_changes == 1:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            return False

    """ Function to delete user from database by name
        Arguments:
            name: Name of user to delete
    """
    def delete_by_name(self, name):
        try:
            if name:
                sql = "DELETE FROM "+ db.sqlite_db['table'] +" where name = ?"
                args = [name]
                self.curs.execute(sql, args)
                self.conn.commit()
                if self.conn.total_changes >= 1:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            return False

    """ Function to delete user from database by number
        Arguments:
            number: Name of user to delete
    """
    def delete_by_number(self, number):
        try:
            if number:
                sql = "DELETE FROM "+ db.sqlite_db['table'] +" where phone_number = ?"
                args = [number]
                self.curs.execute(sql, args)
                self.conn.commit()
                if self.conn.total_changes >= 1:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            return False

    """ Function to get all users from database
    """
    def get_users(self):
        try:
            sql = "SELECT name, phone_number from "+ db.sqlite_db['table']
            row = self.curs.execute(sql)
            return row
        except Exception as e:
            return False
