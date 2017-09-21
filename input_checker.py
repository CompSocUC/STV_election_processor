from pathlib import Path
from classes import Vote, Role, Member, Position, CandidateVote
import csv
import re
import json

MEMBERS_FILE_PATH_DEFAULT = "members.csv"
MEMBERS_UCCODE_COLUMN_NAME_DEFAULT = "UC Username"
USECODE_REGEX = "[a-zA-Z]{3,4}[0-9]{2,3}"

VOTES_FILE_PATH_DEFAULT = "votes.csv"
VOTES_UCCODE_COLUMN_NAME_DEFAULT = "What is your UC usercode (abc123)"
POSITION_REGEX = "[a-zA-Z\s]+\[[a-zA-Z\s]+\]"

ROLES_FILE_PATH_DEFAULT = "roles.json"

VOTE_VALUE_REGEX = "([0-9],\s)*[0-9]"


def check_match_for_usercode_format(value):
    """Check to see if the usercode supplied matches the expected format.

    Args:
        value (str): The usercode to validate.

    Returns:
        bool: True if the usercode is valid, False otherwise.


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
    >>> check_match_for_usercode_format(" abc123")
    False
    >>> check_match_for_usercode_format("abc123 ")
    False
    >>> check_match_for_usercode_format(" abc123 ")
    False
    >>> check_match_for_usercode_format("abc 123")
    False
    """

    if type(value) is str and re.fullmatch(USECODE_REGEX, value) is not None:
        return True

    return False


def check_if_position_vote(value):
    """Check to see if the position supplied matches the expected format.

    Args:
        value (str): The position to validate.

    Returns:
        bool: True if the position is valid, False otherwise.


    >>> check_if_position_vote("Pres [person]")
    True
    >>> check_if_position_vote("Pres")
    False
    >>> check_if_position_vote("Pres[person]")
    True
    >>> check_if_position_vote("[person]")
    False
    >>> check_if_position_vote("Bad")
    False
    >>> check_if_position_vote(12)
    False
    >>> check_if_position_vote("[fail] bad")
    False
    >>> check_if_position_vote(None)
    False
    """

    if type(value) is str and re.fullmatch(POSITION_REGEX, value) is not None:
        return True

    return False


def check_vote_value(value):
    """Check to see if the vote sequence supplied matches the expected format.

    Args:
        value (str, int): The vote to validate.

    Returns:
        bool: True if the vote sequence is valid, False otherwise.


    >>> check_vote_value("")
    True
    >>> check_vote_value("1")
    True
    >>> check_vote_value("1, 2")
    True
    >>> check_vote_value("3, 5")
    True
    >>> check_vote_value(1)
    True
    >>> check_vote_value(12)
    True
    >>> check_vote_value("bad")
    False
    >>> check_vote_value(None)
    True
    """

    if type(value) is int or value is None or \
       (type(value) is str and value == ''):
        return True

    if type(value) is str and \
       re.fullmatch(VOTE_VALUE_REGEX, value) is not None:
        return True

    return False


def read_members(stv):
    """Read members from a csv file, this function extracts all of the member
    usercodes from the file and stores them in the stv object"""

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

        if not check_match_for_usercode_format(row[user_code_column]):
            raise Exception("Error, it appears the column selected is not "
                            "the usercode, usercodes should match the regex {}"
                            .format(USECODE_REGEX))
        else:
            user_code = row[user_code_column].lower()
            stv.members[user_code] = Member(user_code)

        for row in reader:
            user = row[user_code_column].lower()
            if check_match_for_usercode_format(user):
                stv.members[user] = Member(user)


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
            user_code = row[user_code_column].lower()
            if user_code in stv.members:
                member = stv.members[user_code]
                stv.votes[member] = create_vote(stv, row, member)
            else:
                stv.number_non_member_votes += 1

        for row in reader:
            user_code = row[user_code_column].lower()
            if user_code in stv.members:
                member = stv.members[user_code]
                stv.votes[member] = create_vote(stv, row, member)
            else:
                stv.number_non_member_votes += 1


def read_roles(stv):
    roles_file = input("Path to roles json file, [{}]:"
                       .format(ROLES_FILE_PATH_DEFAULT))

    if roles_file == '':
        roles_file = ROLES_FILE_PATH_DEFAULT

    roles_file_path = Path(roles_file)

    if not roles_file_path.is_file():
        raise FileExistsError("Error, roles file does not exist, or path is "
                              "incorrect")

    with open(roles_file) as roles_json:
        stv.roles = json.load(roles_json, object_hook=class_mapper)


def class_mapper(d):
    return Role(**d)


def create_position(stv, vote, row):

    for key, value in row.items():
        if check_if_position_vote(key):
            position_part = key.split('[')
            position_name = position_part[0].strip()

            if position_name not in vote.positions:
                role = match_role(stv, position_name)
                if role is None:
                    raise Exception("Role not found, although is was of a \
                                    valid format.")
                position = Position(role)
                vote.positions[position_name] = position

            else:
                position = vote.positions[position_name]

            position_candidate = position_part[1].split(']')[0].strip()
            candidate_vote = CandidateVote(position_candidate)
            candidate_vote.value = get_valid_vote_value(value)

            position.candidate_votes.append(candidate_vote)


def create_vote(stv, row, member):
    vote = Vote(member)
    create_position(stv, vote, row)

    return vote


def get_valid_vote_value(value):
    if not check_vote_value(value):
        raise Exception("Vote did not match validator")

    if value is None or value == '':
        return None
    possible_values = value.split(',')
    possible_values = map(str.strip, possible_values)

    return min(possible_values)


def match_role(stv, role_name):
    for role in stv.roles:
        if role.column_name == role_name:
            return role
    return None


def get_input(stv):
    read_members(stv)
    read_roles(stv)
    read_votes(stv)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
