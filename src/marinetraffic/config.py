import argparse
from os import path

WINDFARMS_FPATH = "../../data/wind-farms/meta/wind-farms-2.txt"

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

def parse_args() -> dict:
    """
    parse_args -> dict

    instantiate an argument parser object
    to parse the command line argument supplied by the user

    returns a dictionary containing all parsed command line options
    
    """
    argp = argparse.ArgumentParser()

    argp.add_argument(
        '-i',
        '--input-dir',
        help='input directory containing data files', 
        default=path.curdir
    )
    argp.add_argument(
        '-p',
        '--input-pattern',
        help='input pattern used to glob data files',
        default='*.csv'
    )
    argp.add_argument(
        '-o',
        '--output-dir',
        help='output directory, defaults to the current working directory',
        default=path.curdir
    )
    argp.add_argument(
        '-l',
        '--logfile',
        help='logfile to log activities by. default is stdout.',
        default=''
    )
    argp.add_argument(
        '-v',
        '--verbose',
        help='if provided, the logging level will be set to DEBUG',
        action='store_true',
        default=False
    )

    return argp.parse_args().__dict__
