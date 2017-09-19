
def validate_votes(stv):
    validate_membership(stv)


def validate_membership(stv):
    for usercode in stv.votes.copy():
        if usercode not in stv.members:
            del stv.votes[usercode]
            stv.number_non_member_votes += 1


def report_number_invalid_votes(stv):
    total_votes = len(stv.votes) + stv.number_non_member_votes
    print("In total {} votes were cast, {}, {:.2f}% were not members of "
          "CompSoc".format(total_votes, stv.number_non_member_votes,
                           (stv.number_non_member_votes / total_votes) * 100))


def report_voter_turnout(stv):
    print("Turnout for election, {:.2f}%, number of members {:d}, number of "
          "voters {:d}".format((len(stv.votes) / len(stv.members)) * 100,
                               len(stv.members), len(stv.votes)))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
