import argparse

from hanzipy.decomposer import HanziDecomposer
decomposer = HanziDecomposer()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("char")
    args = parser.parse_args()

    print(decomposer.get_characters_with_component(args.char))


