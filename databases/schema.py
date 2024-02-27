# Defines the schema for the QuantumPioneer databases
from peewee import (
    SqliteDatabase,
    Model,
    BlobField,
    TextField,
    FloatField,
    IntegerField,
    BooleanField,
)

# defer to class instantiation
PLACEHOLDER_DB = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = PLACEHOLDER_DB


class GenericResults(BaseModel):
    source = TextField(unique=True)
    route_section = TextField(null=True)
    charge = IntegerField(null=True)
    multiplicity = IntegerField(null=True)


class DLPNOResults(GenericResults):
    energy = FloatField(null=True)
    run_time = FloatField(null=True)
    input_coordinates = BlobField(null=True)


class COSMOResults(DLPNOResults):
    ...


class DFTResults(GenericResults):
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


class SemiEmpiricalResults(DFTResults):
    ...
