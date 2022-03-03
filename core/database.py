from datetime import datetime
import sqlite3


class Database:
    def __init__(self):
        pass        

    def name(self):
        return 'globeexplorerdb'

    def connect(self):
        return sqlite3.connect(self.name())

    def cursor(self, con):
        return con.cursor()

    def get_time(self):
        return str(datetime.now())

    def save_and_close(self, con):
        con.commit()
        con.close()

    def create_initial_tables(self):
        con = self.connect()
        cur = self.cursor(con)

        cur.execute('''CREATE TABLE domains
            (time text, domain text)''')

        cur.execute('''CREATE TABLE urls
            (time text, url text)''')

        cur.execute('''CREATE TABLE vulnerabilities
            (time text, url text, name text, command text, log text, assertion_type text, assertion_value text)''')

        cur.execute('''CREATE TABLE errors
            (time text, url text, name text, command text, log text)''')

        self.save_and_close(con)

    def add_domain(self, domain):
        con = self.connect()
        cur = self.cursor(con)
        time = self.get_time()

        cur.execute("INSERT INTO domains VALUES (?,?)", (
            time, domain
        ))

        self.save_and_close(con)

    def add_url(self, url):
        con = self.connect()
        cur = self.cursor(con)
        time = self.get_time()

        cur.execute("INSERT INTO urls VALUES (?,?)", (
            time, url
        ))

        self.save_and_close(con)

    
    def add_vulnerability(self, url, name, command, log, assertion_type, assertion_value):
        con = self.connect()
        cur = self.cursor(con)
        time = self.get_time()

        cur.execute("INSERT INTO vulnerabilities VALUES (?,?,?,?,?,?,?)", (
            time, url, name, command, log, assertion_type, assertion_value
        ))

        self.save_and_close(con)

    def add_error(self, url, name, command, log):
        con = self.connect()
        cur = self.cursor(con)
        time = self.get_time()

        cur.execute("INSERT INTO urls VALUES (?,?)", (
            time, url, name, command, log
        ))

        self.save_and_close(con)

    def get_domains(self):
        con = self.connect()
        con.row_factory = lambda cursor, row: row[0]
        cur = self.cursor(con)

        domains = cur.execute('SELECT domain FROM domains').fetchall()
        self.save_and_close(con)

        return domains

    def get_urls(self):
        con = self.connect()
        con.row_factory = lambda cursor, row: row[0]
        cur = self.cursor(con)

        urls = cur.execute('SELECT url FROM urls').fetchall()
        self.save_and_close(con)
        
        return urls
