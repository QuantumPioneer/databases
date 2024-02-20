import pickle

# dill, peewee, and tqdm are all single-library dependencies
from peewee import SqliteDatabase, Model, BlobField, TextField, IntegerField, BooleanField, FloatField


db = SqliteDatabase(None)  # defer to class instantiation


class BaseModel(Model):
    class Meta:
        database = db


class Results(BaseModel):
    id = IntegerField(unique=True)
    # file from which the data was retrieved
    source = TextField(unique=True)

    # fields saved as interpretable
    route_section = TextField(null=True)
    charge = IntegerField(null=True)
    multiplicity = IntegerField(null=True)
    max_steps = IntegerField(null=True)
    normal_termination = BooleanField(null=True)
    cpu_time = FloatField(null=True)
    wall_time = FloatField(null=True)
    e0_h = FloatField(null=True)
    hf = FloatField(null=True)
    zpe_per_atom = FloatField(null=True)
    e0_zpe = FloatField(null=True)
    gibbs = FloatField(null=True)

    # array fields saved as Pickles
    scf = BlobField(null=True)
    recovered_energy = BlobField(null=True)
    frequency_modes = BlobField(null=True)
    frequencies = BlobField(null=True)
    std_forces = BlobField(null=True)
    std_xyz = BlobField(null=True)
    xyz = BlobField(null=True)

    def unpickle(item):
        try:
            return pickle.loads(item)
        except:
            return None

    def __iter__(self, truncated=False):

        if truncated:
            return iter(
                (
                    self.id,
                    self.source,
                    self.route_section,
                    self.charge,
                    self.multiplicity,
                    self.max_steps,
                    self.normal_termination,
                    self.cpu_time,
                    self.wall_time,
                    self.e0_h,
                    self.hf,
                    self.zpe_per_atom,
                    self.e0_zpe,
                    self.gibbs,
                    None if not Results.unpickle(self.scf) else Results.unpickle(self.scf)[-1],
                    Results.unpickle(self.recovered_energy),
                    None if not Results.unpickle(self.frequency_modes) else Results.unpickle(self.frequency_modes)[:3],
                    Results.unpickle(self.frequencies),
                    Results.unpickle(self.std_forces),
                    Results.unpickle(self.std_xyz),
                    Results.unpickle(self.xyz),
                )
            )

        else:
            return iter(
                (
                    self.source,
                    self.route_section,
                    self.charge,
                    self.multiplicity,
                    self.max_steps,
                    self.normal_termination,
                    self.cpu_time,
                    self.wall_time,
                    self.e0_h,
                    self.hf,
                    self.zpe_per_atom,
                    self.e0_zpe,
                    self.gibbs,
                    Results.unpickle(self.scf),
                    Results.unpickle(self.recovered_energy),
                    Results.unpickle(self.frequency_modes),
                    Results.unpickle(self.frequencies),
                    Results.unpickle(self.std_forces),
                    Results.unpickle(self.std_xyz),
                    Results.unpickle(self.xyz),
                )
            )


# todo: write a connect/close decorator to wrap database reads


class TriState20:
    def __init__(self, db_path):
        db.init(db_path)
        self.id = 1

    def get_n_converged_random(self, n, truncated=False):
        db.connect()
        query = Results.select().where(Results.id < self.id + n, Results.id >= self.id)
        out = [tuple(iter(res, truncated=truncated)) for res in query]
        db.close()
        self.id += n
        return out
    
    def get_converged_partitioned(self, offset, limit, truncated=False):
        db.connect()
        query = Results.select().order_by(Results.id).offset(offset).limit(limit)
        out = [tuple(iter(res, truncated=truncated)) for res in query]
        db.close()
        return out
    
    def get_converged_by_id(self, entry_id, truncated=False):
        db.connect()
        query = Results.select().where(Results.id == entry_id)
        out = [tuple(iter(res, truncated=truncated)) for res in query]
        db.close()
        return out


if __name__ == "__main__":
    ts20 = TriState20("/home/jackson/dft_data_v2.db")
    print(ts20.get_n_converged(10))
    print(ts20.get_n_converged(10))
