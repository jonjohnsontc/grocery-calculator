from ingest import Ingest, INGEST_SQL_FOLDER
from reader import read_sql


class TargetIngest(Ingest):

    def copy_data(self, location):
        ingest_query = read_sql(f"{INGEST_SQL_FOLDER}/copy_target.sql")
        result = self.db.con.execute_query(ingest_query, location)
        num_rows = result[0][0]
        return num_rows

    def preprocess(self):
        return

    def update(self):
        return


if __name__ == "__main__":
    pass
