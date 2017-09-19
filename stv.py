from input_checker import get_input
from classes import STV
from processor import (validate_votes, report_number_invalid_votes,
                       report_voter_turnout)


def main():
    stv = STV()
    get_input(stv)

    validate_votes(stv)

    report_number_invalid_votes(stv)

    report_voter_turnout(stv)


main()
