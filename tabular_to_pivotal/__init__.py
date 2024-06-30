from tabular_to_pivotal.load_and_transform import load_and_transform


def main() -> None:
    import sys

    if len(sys.argv) != 3:
        print("Usage: tabular_to_pivotal <input_file> <output_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    load_and_transform(input_file, output_file)


if __name__ == "__main__":
    main()
