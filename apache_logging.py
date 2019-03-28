from pathlib import Path
import re
import helper_functions as hf


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
    log         = hf.remap(log, "bytes", lambda b: int(b) if b != '-' else 0)
    log         = hf.remap(log, "status", int)

    return log


def get_apache_data():
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

    log_lines   = hf.get_lines(input_filename, filepath)
    log_list    = line_to_log(log_lines)

    #write_out(log_list, output_filename)
    return log_list
