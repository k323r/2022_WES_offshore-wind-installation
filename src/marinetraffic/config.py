import argparse
from os import path

WINDFARMS_FPATH = "../../data/windfarms/windfarms.csv"

COLUMN_NAMES = [
    'mmsi',
    'latitude',
    'longitude',
    'speed',
    'heading',
    'course',
    'status',
    'timestamp',
]

OUTPUT_COLUMN_NAMES = [
    'mmsi',
    'epoch',
    'latitude',
    'longitude',
    'speed',
    'heading',
    'course',
    'status',
]


VESSEL_NAMES = {
    253366000 : "Vole au Vent",
    218657000 : "Vole au Vent",
    5179000   : "Aeolus",
    245179000 : "Aeolus",
    215644000 : "Blue Tern",
    235090598 : "Blue Tern",
    229080000 : "Bold Tern",
    229044000 : "Brave Tern",
    253609000 : "Taillevent",
    246777000 : "MPI Resolution",
    245924000 : "MPI Adventure",
    219019002 : "Sea Challenger",
    218389000 : "Thor",
    219456000 : "Sea Installer",
    253586000 : "Apollo",
    218781000 : "Innovation",
    218319000 : "Wind Lift 1",
    370582000 : "GMS Endeavour",
    219615000 : "Wind Server",
    241568000 : "Sea Jack",
    235098723 : "Seajacks Zaratan-FRC",
    431050000 : "Seajacks Zaratan",
    356068000 : "Seajacks Scylla",
    370262000 : "Seajacks Leviathan",
    370239000 : "Seajacks Hydra",
    370267000 : "Seajacks Kraken",
}


