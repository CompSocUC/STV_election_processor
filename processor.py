

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

    run_challenge(votes_for_role, role, stv, [])


def run_challenge(position_votes, role, stv, eliminated=[]):
    """For a given role find the victors"""
    rankings = {}
    num_votes = 0
    for position_vote in position_votes:
        position_vote.candidate_votes.sort(key=lambda candidate_vote: candidate_vote.value)
        # take the first value of the sorted list
        # This should be the candidates lowest vote, as in their first preference.

        # if a role cannot be held in conjunction, then we need to make sure that a candidate does not already hold a position on the committee.
        index = 0
        if not role.held_in_conjuction:
            while index < len(position_vote.candidate_votes):
                candidate = position_vote.candidate_votes[index].name
                if candidate not in stv.victors and candidate not in eliminated:
                    break
                index += 1

        # check to see if a vote is only for one candidate and that candidate already has a position in the committee
        # So the effective vote does not count
        if index < len(position_vote.candidate_votes):
            candidate = position_vote.candidate_votes[index].name
            num_votes += 1
        # Get the name of the candidate, check to see if we have seen the candidate before
        # If not then add them to dict of rankings

            if candidate not in rankings:
                rankings[candidate] = 1

            rankings[candidate] += 1

    total_votes = num_votes


    ranks = sorted(rankings.items(), key=lambda x: x[1], reverse=True)

    min_percentage = (role.number_of_positions / (role.number_of_positions + 1)) / role.number_of_positions

    victors_message = ""
    vote_majority = True
    victors = []
    for _ in range(0, role.number_of_positions):
        if (ranks[_][1] / total_votes) >= min_percentage:
            victors_message += "Role: {}, Victor: {}, with {:.2f}%\n".format(role.name, ranks[_][0], (ranks[_][1] / total_votes) * 100)
            victors.append(ranks[_][0])
        else:
            vote_majority = False
            break

    if not vote_majority:
        # clear message
        victors_message = ""
        # elimindate lowest person
        # check the length of the candidates left, could have situation where there is only one candidate and no confidence.
        # assume that the no confidence candidate always exists.
        if (len(ranks) - 1) <= role.number_of_positions:
            # find the no confidence
            min_vote_threshold = 0
            for name, votes in ranks:
                if name == "No Confidence":
                    min_vote_threshold = votes
                    break
            # check to make sure that other candidates have at least more votes than no confidence
            for name, votes in ranks:
                if votes >= min_vote_threshold and name != "No Confidence":
                    victors_message += "Role: {}, Victor: {}, with {:.2f}%\n".format(role.name, name, (votes / total_votes) * 100)
                    victors.append(name)
                else:
                    if name != "No Confidence":
                        print("Well shit, what happens now")
        else:
            # find the lowest person that is not no confidence and add them to elimindated list
            # rerun challenge
            index = -1
            while index > (len(ranks) * -1):
                if ranks[index][0] != "No Confidence":
                    eliminated.append(ranks[index][0])
                    break
                index -= 1

            run_challenge(position_votes, role, stv, eliminated)
    stv.victors += victors
    print(victors_message)


def validate_votes(stv):
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
