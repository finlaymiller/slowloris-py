import gzip
from pathlib import Path
import re
import json


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


def line_to_log(lines):
    """
    Convert lines read from file to a list of JSON formatted dictionaries.
    Uses regex to parse lines.

    :param lines: list of lines to convert.
    :return: list of dictionaries
    """
    col_names   = ('host', 'identity', 'user', 'datetime',
                   'method', 'request', 'proto', 'status',
                   'bytes', 'referrer', 'user-agent')
    regex_ptn   = r'(\S+) (\S+) (\S+) \[(.*?)\] ' \
                  r'"(\S+) (\S+) (\S+)" (\S+) (\S+)' \
                  r'(\S+) (\S+)'

    reg_pat     = re.compile(regex_ptn)
    groups      = (reg_pat.match(line) for line in lines)
    tuples      = (g.groups() for g in groups if g)
    log         = (dict(zip(col_names, t)) for t in tuples)
    log         = remap(log, "bytes", lambda b: int(b) if b != '-' else 0)
    log         = remap(log, "status", int)

    return log


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


def write_out(log, filename):
    """
    Writes all logs and lines to output file in JSON format

    :param log:         List of logs to write.
    :param filename:    Name of file to write to.
    :return: None.
    """
    with open(filename, 'w') as f:
        for entry in log:
            json.dump(entry, f)
            f.write("\n")
        f.close()

        if filename.isfile():
            print("Logs successfully written to ", Path.cwd())
        else:
            print("Failed to write to file.")


def main():
    """
    Gets all apache access logs in a directory and prints them to a JSON file.
    :return: None.
    """
    input_filename  = "access.*"
    output_filename = "log_summary.json"

    # uncomment lines below depending on workspace
    #filepath   = Path("/var/log/apache2")                                                      # raspberry pi
    #filepath   = Path("C:/Users/minla/OneDrive/Documents/Raspberry Pi/Apache Logs")            # surface
    filepath   = Path("C:/Users/Finlay Miller/OneDrive/Documents/Raspberry Pi/Apache Logs")    # desktop

    log_lines   = get_lines(input_filename, filepath)
    log_list    = line_to_log(log_lines)

    write_out(log_list, output_filename)


if __name__ == '__main__':
    main()
