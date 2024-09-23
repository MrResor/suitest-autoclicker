import argparse

# setup the parser for autoclicker arguments
parser = argparse.ArgumentParser(
                    prog='Suitest Autoclicker',
                    description='Translates strings to clicks on remote to input them on the device'
                    )

# TODO can be created by reading contents of keyboards file instead of filling them manually, this will
# remove need of checking if file with given name exists
parser.add_argument('platform', choices=['sky', 'sagemcom', 'webos'], help="platform of the device")
parser.add_argument('string', help="text that should be translated")