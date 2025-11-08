import sqlite3  # Todo: Move over to aiosqlite

# Todo: Connection pooling

class _Database:
    def __init__(self):
        self.__DB_LOCATION = "/app/data/denbot.sqlite"
        self.__connection = sqlite3.connect(self.__DB_LOCATION)
        self.cur = self.__connection.cursor()

    def __del__(self):
        self.__connection.close()

    def execute(self, new_data, parameters = None):
        try:
            if parameters:
                result = self.cur.execute(new_data, parameters)
            else:
                result = self.cur.execute(new_data)
            return result.fetchone()
        except Exception as e:
            print(f"Failed to execute query: {new_data} with error: {e}")

    def executemany(self, many_new_data):
        self.cur.executemany(many_new_data)

    def commit(self):
        try:
            self.__connection.commit()
        except Exception as e:
            print(f"Failed to commit changes with error: {e}")


class DB:
    def add_guild(guild):
        db = _Database()
        db.execute(f"INSERT OR IGNORE INTO servers (guild_id) VALUES ({guild});")
        db.commit()

    def create_database():
        db = _Database()
        db.execute(
            "CREATE TABLE IF NOT EXISTS settings (guild_id NOT NULL, setting NOT NULL, value, UNIQUE(guild_id, setting));"
        )
        db.commit()

    def update_setting(guild_id, setting, value):
        db = _Database()
        db.execute(
            f"INSERT INTO settings (guild_id,setting,value) VALUES ({guild_id}, '{setting}', {value}) ON CONFLICT (guild_id, setting) DO UPDATE SET value={value};"
        )
        db.commit()

    def get_setting(guild_id, setting_name):
        db = _Database()
        return db.execute(
            f"SELECT value FROM settings WHERE guild_id LIKE {guild_id} AND setting LIKE '{setting_name}';"
        )[0]
