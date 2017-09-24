from input_checker import get_input
from classes import STV
from processor import (report_number_invalid_votes, report_votes, report_results,
                       validate_votes, report_voter_turnout, report_roles)


def main():
    stv = STV()
    get_input(stv)

    validate_votes(stv)
    print()
    report_number_invalid_votes(stv)
    print()
    report_voter_turnout(stv)
    print()
    # report_roles(stv)
    report_results(stv)


main()
