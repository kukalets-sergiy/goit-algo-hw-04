"""Recursively copy files and group them by extension.

To run this script, use the command line to navigate to the directory containing the script and execute it with the
source directory as an argument. Optionally, you can specify a destination directory; if not provided,
it defaults to "dist".
Type in command line:
python3 task_1.py test_data
The function will recursively copy all files from the source directory to the destination directory,
grouping them by their file extensions.
"""

import argparse
import shutil
import sys
from pathlib import Path


def extension_directory(file_path: Path) -> str:
    """Return a safe directory name for a file extension."""
    return file_path.suffix.lower().lstrip(".") or "no_extension"


def unique_destination(file_path: Path) -> Path:
    """Return a non-conflicting destination path."""
    # If the file path does not exist, return it as is.
    if not file_path.exists():
        return file_path

    # counter for generating unique file names
    counter = 1
    # Loop until a unique file name is found.
    while True:
        # Generate a candidate file path with a counter appended to the stem.
        candidate = file_path.with_name(
            f"{file_path.stem}_{counter}{file_path.suffix}" # file_path.stem is the name of the file without extension
        )
        # If the candidate file path does not exist, return it.
        if not candidate.exists():
            return candidate
        counter += 1


def sort_files(source: Path, destination: Path) -> int:
    """Recursively copy files from source into extension directories. Return the number of copied files."""
    # Initialize a counter for the number of copied files.
    copied_files = 0
    try:
        # Get a sorted list of entries in the source directory, ignoring case.
        # source.iterdir() returns an iterator of Path objects for each entry in the source directory.
        entries = sorted(source.iterdir(), key=lambda path: path.name.lower())
    # Handle the case where the source directory cannot be read.
    except OSError as error:
        # sys.stderr is a file object that points to the standard error stream. It is used to print error messages.
        print(f"Cannot read {source}: {error}", file=sys.stderr)
        return copied_files

    # Iterate over each entry in the sorted list of entries.
    for entry in entries:
        # .resolve() returns the absolute path of the entry, resolving any symbolic links.
        if entry.resolve() == destination.resolve():
            continue

        try:
            # If the entry is a directory.
            if entry.is_dir():
                # Call sort_files recursively on the directory and add the number of copied files to the counter.
                copied_files += sort_files(entry, destination)
            elif entry.is_file():
                # If the entry is a file, determine the target directory based on the file's extension.
                target_directory = destination / extension_directory(entry)
                # Create the target directory if it does not exist, including any necessary parent directories.
                target_directory.mkdir(parents=True, exist_ok=True)
                # Determine a unique destination path for the file to avoid overwriting existing files.
                target = unique_destination(target_directory / entry.name)
                # Copy the file to the target location, preserving metadata.
                shutil.copy2(entry, target)
                # Increment the counter for copied files.
                copied_files += 1
                # Print a message indicating the file has been copied.
                print(f"Copied: {entry} -> {target}")
        # OSError is raised for issues like permission errors or file not found errors.
        except OSError as error:
            # file=sys.stderr is used to print the error message to the standard error stream instead of the standard output.
            print(f"Cannot process {entry}: {error}", file=sys.stderr)

    return copied_files


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    # Create an ArgumentParser object to handle command-line arguments.
    parser = argparse.ArgumentParser(
        description="Copy files recursively and sort them by extension."
    )
    # Add a positional argument for the source directory, which is required.
    parser.add_argument("source", type=Path, help="source directory")
    # Add an optional positional argument for the destination directory, which defaults to "dist" if not provided.
    parser.add_argument(
        "destination",
        type=Path,
        nargs="?", # nargs="?" means that the argument is optional and can be omitted.
        default=Path("dist"),
        help="destination directory (default: dist)",
    )
    # Parse the command-line arguments and return them.
    return parser.parse_args()


def main() -> None:
    """Validate arguments and start recursive copying."""
    # Parse command-line arguments.
    arguments = parse_arguments()
    # Resolve the source and destination paths to their absolute forms.
    source = arguments.source.resolve()
    # Resolve the destination path to its absolute form.
    destination = arguments.destination.resolve()

    # If not a directory, print an error message to standard error and exit with a non-zero status code.
    if not source.is_dir():
        print(f"Source directory does not exist: {source}", file=sys.stderr)
        raise SystemExit(1)

    # Create the destination directory if it does not exist, including any necessary parent directories.
    destination.mkdir(parents=True, exist_ok=True)
    # Call the sort_files function to copy files and get the number of copied files.
    copied_files = sort_files(source, destination)
    print(f"Copied files: {copied_files}")


if __name__ == "__main__":
    main()
