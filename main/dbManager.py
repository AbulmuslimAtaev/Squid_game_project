import sqlite3


class dbManager:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

    def set_data(self, table, to_set, to_where):
        seq = f"UPDATE {table} SET {', '.join([f'{i}={to_set[i]}' for i in to_set])} "
        seq += f"WHERE {' AND '.join([f'{i} {to_where[i]}' for i in to_where])}"
        self.cur.execute(seq)
        self.con.commit()

    def get_data(self, table, to_select, to_where={}):
        seq = f"SELECT {', '.join([i for i in to_select])} "
        seq += f"FROM {table} "
        if to_where:
            seq += f"WHERE {' AND '.join([f'{i} {to_where[i]}' for i in to_where])} "
        data = self.cur.execute(seq).fetchall()
        return data
