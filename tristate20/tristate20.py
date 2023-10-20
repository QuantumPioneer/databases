import os

# dill, peewee, and tqdm are all single-library dependencies
import dill
from peewee import SqliteDatabase, Model, BlobField, TextField
# from fastlogfileparser.gaussian import fast_gaussian_logfile_parser as fglp
# from fastlogfileparser.gaussian.fast_gaussian_logfile_parser import ALL_FIELDS

# print(ALL_FIELDS)
db = SqliteDatabase(None)  # defer to class instantiation


class BaseModel(Model):
    class Meta:
        database = db


class Results(BaseModel):
    source = TextField(unique=True)
    result = BlobField()


# todo: write a connect/close decorator to wrap database reads

class TriState20:
    def __init__(self, db_path):
        db.init(db_path)

    def get_all(self):
        db.connect()
        out = Results.get()
        # deserialize
        source, result = out.source, dill.loads(out.result)
        db.close()
        return source, result


if __name__ == "__main__":
    ts20 = TriState20("/home/jackson/Desktop/parser_test.db")
    print(ts20.get_all())
