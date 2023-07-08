import argparse

def initialize_parser():
    parser = argparse.ArgumentParser(
        prog="GoogleImageScraperArgParser",
        description="parser for Google Image Scraper command line args"
    )

    parser.add_argument("--searchkeys", nargs="+", default=["default"], help="Provide a list of search keys. [EXAMPLE: \`--searchkeys dog cat raccoon]\`")
    parser.add_argument("--imagecount", type=int, default=5, help="The number of images to return for each search key. [EXAMPLE: \`--imagecount 50\`]")
    parser.add_argument("--headless", action="store_true", help="Chrome GUI behaviour. If True, there will be no GUI. Defaults to False. [EXAMPLE: \`--headless\`]")
    parser.add_argument("--minres", nargs=2, default=[0, 0], help="Minimum desired image resolution. Parser will convert to an (x, y) value pair. [EXAMPLE: \`--minres 500 500\`]")
    parser.add_argument("--maxres", nargs=2, default=[9999,9999], help="Maximum desired image resolution. Parser will convert to an (x, y) value pair. [EXAMPLE: \`--maxres 2000 2000\`]")
    parser.add_argument("--numworkers", type=int, default=1, help="Number of workers used for parallel processing. [EXAMPLE: \`--numworkers 5\`]")
    parser.add_argument("--keepfilename", action="store_true", help="Keeps original URL image filenames. Defaults to False. [EXAMPLE:\`--keepfilename\`]")
    parser.add_argument("--colabs", action="store_false", help="Flag to tell script that it's running in a Colabs environment.")

    return parser

def parse_args(parser: argparse.ArgumentParser): 
    args = parser.parse_args()
    return args