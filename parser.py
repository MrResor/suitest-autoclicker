import argparse
from os import walk

# setup the parser for autoclicker arguments
parser = argparse.ArgumentParser(
                    prog='Suitest Autoclicker',
                    description='Translates strings to clicks on remote to input them on the device'
                    )

# checks json files in keyboard folders and uses them to populate choices of platform argument
filenames = next(walk('./keyboards'), (None, None, []))[2] 
choices = [filename.split('.json')[0] for filename in filenames if filename.endswith('.json')]
choices.sort()

parser.add_argument('platform', choices=choices, help="platform of the device")
parser.add_argument('string', help="text that should be translated")