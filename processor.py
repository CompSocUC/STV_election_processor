

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


def report_votes(stv):
    for member, item in stv.votes.items():
        print(repr(item))


def report_results(stv):
    for role in stv.roles:
        role_victors(role, stv)


def role_victors(role, stv):
    """Gather all the results for a particular role"""
    votes_for_role = []
    for vote in stv.votes.values():
        position = vote.positions[role.column_name]
        if len(position.candidate_votes) > 0:
            votes_for_role.append(position)
    run_challenge(votes_for_role, role)


def run_challenge(position_votes, role):
    """Array of positions"""
    rankings = {}
    for position_vote in position_votes:
        position_vote.candidate_votes.sort(key=lambda candidate_vote: candidate_vote.value)
        # take the first value of the sorted list
        candidate = position_vote.candidate_votes[0].name
        if candidate not in rankings:
            rankings[candidate] = 0

        rankings[candidate] += 1

    total_votes = len(position_votes)
    ranks = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
    print("Role: {}, Victor: {}, with {:.2f}%".format(role.name, ranks[0][0], (ranks[0][1] / total_votes) * 100))


def validate_votes(stv):
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
