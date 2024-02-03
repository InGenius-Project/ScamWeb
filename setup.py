import sqlite3
from constant import DBInfo


def main():
    conn = sqlite3.connect(DBInfo.connectname)
    print(f"Local Database: {DBInfo.connectname} Created.")

    cursor = conn.cursor()
    with open(DBInfo.init_script_path, "r") as scripts_file:
        sql_script = scripts_file.read()
    cursor.executescript(sql_script)
    print("Database Init Succeed.")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
