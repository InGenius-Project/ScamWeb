import sqlite3

from pydantic_core.core_schema import nullable_schema
from constant import DBInfo


class DataEntity:
    class LabelType:
        NOTSCAM = 0
        ISSCAM = 1
        NOTSURE = 2
        NOCOMMENT = 3

    def __init__(self, id: str, content: str, label: int = LabelType.NOCOMMENT):
        self.Id = id
        self.Content = content
        self.Label = label


class DataService:
    def __init__(self):
        self.conn = sqlite3.connect(DBInfo.connectname)
        self.cursor = self.conn.cursor()

    def save_change(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def get_all(self):
        command = "SELECT * FROM Data;"
        self.cursor.execute(command)
        return self.cursor.fetchall()

    def get_by_id(self, id: str):
        command = "SELECT * FROM Data WHERE id = ?;"
        self.cursor.execute(command, (id,))
        return self.cursor.fetchall()

    def add(self, entity: DataEntity):
        command = "INSERT INTO Data (id, content, label) VALUES (?, ?, ?);"
        insert_data = (entity.Id, entity.Content, entity.Label)
        self.cursor.execute(command, insert_data)

    def add_range(self, entity_list: list[DataEntity]):
        command = "INSERT INTO Data (id, content, label) VALUES (?, ?, ?);"
        insert_data_list = [
            (entity.Id, entity.Content, entity.Label) for entity in entity_list
        ]
        self.cursor.executemany(command, insert_data_list)

    def set_label(self, id: str, label: int):
        command = "UPDATE Data SET label = ? WHERE id = ?;"
        insert_data = (label, id)
        self.cursor.execute(command, insert_data)

    def get_all_id(self):
        command = "SELECT id FROM Data;"
        self.cursor.execute(command)
        result = self.cursor.fetchall()
        id_list = [x[0] for x in result]
        return id_list

    def get_nocomment(self):
        command = "SELECT * FROM Data WHERE label = ? ORDER BY label ASC LIMIT 1;"
        self.cursor.execute(command, (DataEntity.LabelType.NOCOMMENT,))
        result = self.cursor.fetchall()
        if len(result) == 0:
            return None
        return result[0]
