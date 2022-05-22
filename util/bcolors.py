class _bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_success(msg, printCrLf=True):
    end = ''
    if (printCrLf):
        end = '\n'
    else:
        end = ''

    print(_bcolors.OKGREEN + msg + _bcolors.ENDC, end=end)


def print_warning(msg, printCrLf=True):
    end = ''
    if (printCrLf):
        end = '\n'
    else:
        end = ''

    print(_bcolors.WARNING + msg + _bcolors.ENDC, end=end)


def print_error(msg, printCrLf=True):
    end = ''
    if (printCrLf):
        end = '\n'
    else:
        end = ''

    print(_bcolors.FAIL + msg + _bcolors.ENDC, end=end)


def print_normal(msg, printCrLf=True):
    end = ''
    if (printCrLf):
        end = '\n'
    else:
        end = ''

    print(msg, end=end)
