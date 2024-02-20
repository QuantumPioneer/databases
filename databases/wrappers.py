

# add method to insert new columns
# add new keys, like atom-mapped smiles etc.
# 
# remove the fpath column in production release



class AbstractWrapper:
    def __init__(self):
        self.conn = None
        self.already_selected = None

    def get_ids(self, datatype: DATATYPES = "list", with_replacement: bool = False):
        """Return a list of all of the row GUIDs in the database."""

    def get_next(self, datatype: DATATYPES = "list", with_replacement: bool = False):
        """Iterates through database, saving current position."""

    def get_n_next(
        self,
        n: int,
        datatype: DATATYPES = "list",
        with_replacement: bool = False,
    ):
        """Iterates through database, saving current position."""

    def get_random(self, datatype: DATATYPES = "list", with_replacement: bool = False):
        """Gets a random row."""

    def get_n_random(
        self,
        n: int,
        datatype: DATATYPES = "list",
        with_replacement: bool = False,
    ):
        """Gets n random rows."""

    def get_all(self, datatype: DATATYPES = "list", with_replacement: bool = False):
        """Loads entire database and returns it (large memory footprint and initial runtime!)"""

    def get_all_in_solvent(
        self,
        datatype: DATATYPES = "list",
        solvent: SOLVENTS = "water",
    ):
        """Loads all entries for a given solvent and return them."""

    def reset_position(self):
        """Sets the position of the get_next back to the beginning of the database"""

    def set_position(self):
        """Sets the current position to the given GUID."""

    def find_dgsolv(self, solvent: str, solute: str):
        """Find the free energy of solvation for the given solute and solvent."""

    def _get_at(self, datatype: DATATYPES = "list", with_replacement: bool = False):
        """Driver helper that retrieves a single row at a given GUID"""

class ORCAWrapper(AbstractWrapper):
    ...

class DFTWrapper(AbstractWrapper):
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
    ts20 = DFTWrapper("/home/jackson/dft_data_v2.db")
    print(ts20.get_n_converged(10))
    print(ts20.get_n_converged(10))