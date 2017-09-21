

def report_number_invalid_votes(stv):
    total_votes = len(stv.votes) + stv.number_non_member_votes
    print("In total {} votes were cast, {}, {:.2f}% were not members of "
          "CompSoc".format(total_votes, stv.number_non_member_votes,
                           (stv.number_non_member_votes / total_votes) * 100))


def report_voter_turnout(stv):
    print("Turnout for election, {:.2f}%, number of members {:d}, number of "
          "voters {:d}".format((len(stv.votes) / len(stv.members)) * 100,
                               len(stv.members), len(stv.votes)))


def report_roles(stv):
    for role in stv.roles:
        print(str(role) + "\n")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
