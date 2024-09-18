import argparse

# setup the parser for autoclicker arguments
parser = argparse.ArgumentParser(
                    prog='Suitest Autoclicker',
                    description='Translates strings to clicks on remote to input them on the device'
                    )

parser.add_argument('platform', choices=['sky', 'sagemcom', 'webos'], help="Platform of the device.")
parser.add_argument('string', help="Text that should be translated.")