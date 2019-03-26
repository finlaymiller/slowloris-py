# Helper functions for Apache server and Raspberry Pi hardware monitoring

import gzip
from pathlib import Path
import csv

def get_files(path):
    """
    Open all files within a directory.

    :param path: Path to files. Will have file information attached to end.
                     e.g. '~/*.txt'
    :return: Generator for open file objects.
    """
    for p in path:
        if p.suffix == '.gz':
            yield gzip.open(p, 'rt')
        else:
            yield open(p, 'rt')
        print("File read from: ", str(p))


def concat(sources):
    """
    Concatenate items from multiple sources into a sequence of items.

    :param sources: Any list object.
    :return: Generator for the objects in said list.
    """
    for src in sources:
        yield from src


def remap(dictseq, name, func):
    """
    Convert dictionary fields to proper values for a sequence of dictionaries.

    :param dictseq: List of dictionaries.
    :param name:    Name (or key) of field to remap.
    :param func:    Remapping function to apply.
    :return:        Dictionaries with fields corrected.
    """
    for field in dictseq:
        field[name] = func(field[name])
        yield field


def get_lines(filename, filepath):
    """
    Extract all lines from all log files within a certain directory.

    :param filename: Name of file to extract data from. Supports wildcards.
    :param filepath: Path to search.
    :return: All lines of all logs in a list.
    """
    names = Path(filepath).rglob(filename)
    files = get_files(names)
    lines = concat(files)

    return lines


def write_out(log_list, filename):
    """
    Writes all logs and lines to output file in JSON format

    :param log_list:    List of logs to write.
    :param filename:    Name of file to write to.
    :return: None.
    """
    with open(filename, 'w') as f:
        csv_out = csv.DictWriter(f, log_list[0].keys())
        csv_out.writeheader()
        csv_out.writerows(log_list)
        f.close()

        logfile = Path(filename)
        if logfile.exists():
            print("Logs successfully written to ", Path.cwd())
        else:
            print("Failed to write to file.")
