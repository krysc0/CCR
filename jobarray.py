import argparse
import os

def create_output_file(index):
    filename = f"{index}.txt"

    # Write content to the file
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write(f"Output file {index} \n")

    print(f"File '{filename}' was created successfully!")

if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Simple Example")

    # Add argument for index
    parser.add_argument("--index", type=str, help="The index to be used as the filename (e.g. 1, 2, 3)")

    # Parse the arguments
    args = parser.parse_args()