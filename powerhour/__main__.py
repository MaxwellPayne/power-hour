from powerhour.generation import generate_powerhour
from powerhour.generation.args import ArgumentParser


def _main():
    arg_parser = ArgumentParser()
    args = arg_parser.parse_args()
    generate_powerhour(args.playlist_url, args.youtube_api_key)


if __name__ == '__main__':
    _main()
