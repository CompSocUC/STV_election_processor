from pathlib import Path
from classes import Vote
import csv
import re

MEMBERS_FILE_PATH_DEFAULT = "members.csv"
MEMBERS_UCCODE_COLUMN_NAME_DEFAULT = "UC Username"
USECODE_REGEX = "[a-zA-Z]{3,4}[0-9]{2,3}"

VOTES_FILE_PATH_DEFAULT = "votes.csv"
VOTES_UCCODE_COLUMN_NAME_DEFAULT = "What is your UC usercode (abc123)"


def check_match_for_usercode_format(value):
    """Check to see if the usercode supplied matches the expected format.
    >>> check_match_for_usercode_format("abc123")
    True
    >>> check_match_for_usercode_format("abc12")
    True
    >>> check_match_for_usercode_format("Adcw12")
    True
    >>> check_match_for_usercode_format("Aada123")
    True
    >>> check_match_for_usercode_format("junk")
    False
    >>> check_match_for_usercode_format(1232)
    False
    >>> check_match_for_usercode_format("1232")
    False
    >>> check_match_for_usercode_format("ab12")
    False
    >>> check_match_for_usercode_format("ab123")
    False
    >>> check_match_for_usercode_format("")
    False
    """

    if type(value) is str and re.match(USECODE_REGEX, value) is not None:
        return True

    return False


def read_members(stv):
    members_file = input("Path to members csv file, [{}]: "
                         .format(MEMBERS_FILE_PATH_DEFAULT))

    if members_file == '':
        members_file = MEMBERS_FILE_PATH_DEFAULT

    members_file_path = Path(members_file)

    # check that the file exists
    if not members_file_path.is_file():
        raise FileExistsError("Error, {} file does not exist, or path "
                              "is incorrect".format(members_file))

    user_code_column = input("What is the name of the user code column in "
                             "the {} file, [{}]: "
                             .format(members_file,
                                     MEMBERS_UCCODE_COLUMN_NAME_DEFAULT))
    if user_code_column == '':
        user_code_column = MEMBERS_UCCODE_COLUMN_NAME_DEFAULT

    with open(members_file, newline='') as members_csv:
        reader = csv.DictReader(members_csv, delimiter=',', quotechar='"')
        row = next(reader)

        if not row[user_code_column]:
            raise Exception("Error, it appears the column selected is not "
                            "the usercode, usercodes should match the regex {}"
                            .format(USECODE_REGEX))
        else:
            stv.members.add(row[user_code_column])

        for row in reader:
            user = row[user_code_column]
            if check_match_for_usercode_format(user):
                stv.members.add(user)


def read_votes(stv):
    votes_file = input("Path to votes csv file, [{}]: "
                       .format(VOTES_FILE_PATH_DEFAULT))

    if votes_file == '':
        votes_file = VOTES_FILE_PATH_DEFAULT

    votes_file_path = Path(votes_file)

    # check that the file exists
    if not votes_file_path.is_file():
        raise FileExistsError("Error, members file does not exist, or path "
                              "is incorrect")

    user_code_column = input("What is the name of the user code column in "
                             "the {} file, [{}]: "
                             .format(votes_file,
                                     VOTES_UCCODE_COLUMN_NAME_DEFAULT))
    if user_code_column == '':
        user_code_column = VOTES_UCCODE_COLUMN_NAME_DEFAULT

    with open(votes_file, newline='') as votes_csv:
        reader = csv.DictReader(votes_csv, delimiter=',', quotechar='"')
        row = next(reader)

        if not row[user_code_column]:
            raise Exception("Error, it appears the column selected is not "
                            "the usercode, usercodes should match the regex {}"
                            .format(USECODE_REGEX))
        else:
            stv.votes[row[user_code_column]] = create_vote(row,
                                                           user_code_column)

        for row in reader:
            stv.votes[row[user_code_column]] = create_vote(row,
                                                           user_code_column)


def create_vote(row, user_code_column):
    vote = Vote(row[user_code_column])

    return vote


def get_input(stv):
    read_members(stv)
    read_votes(stv)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
