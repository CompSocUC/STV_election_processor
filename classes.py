class STV:

    def __init__(self):
        self.members = {}
        self.votes = {}
        self.number_non_member_votes = 0
        self.roles = []
        self.invalidVotes = {}
        self.victors = []


class Member:

    def __init__(self, usercode):
        self.usercode = usercode

    def __repr__(self):
        return "Member({!r})".format(self.usercode)

    def __str__(self):
        return "Member name: {}".format(self.usercode)


class Vote:

    def __init__(self, member):
        self.member = member
        self.positions = {}

    def __repr__(self):
        return "Vote({!r}), positions[{!r}]".format(self.member,
                                                    self.positions)

    def __str__(self):
        return "Vote made by {}".format(self.member)


class Position:

    def __init__(self, role):
        self.role = role
        self.candidate_votes = []

    def __repr__(self):
        return "Position({!r}), candidate_votes[{!r}]"\
            .format(self.role, self.candidate_votes)

    def __str__(self):
        return "Position name: {} with candidate_votes: {}"\
            .format(self.role.name, self.candidate_votes)


class CandidateVote:

    def __init__(self, name):
        self.name = name
        self.value = None

    def __repr__(self):
        return "CandidateVote({!r}), value {!r}".format(self.name, self.value)

    def __str__(self):
        return "Candidate Vote for {}, with a value {}".format(self.name,
                                                               self.value)


class Role:

    def __init__(self, name, column_name, held_in_conjuction=False,
                 number_of_positions=1):
        self.name = name
        self.number_of_positions = number_of_positions
        self.held_in_conjuction = held_in_conjuction
        self.column_name = column_name

    def __str__(self):
        return "Position name: {}\nColumn name: {}\nNumber of available " \
            "positions: {}\nPosition can be held in " \
            "conjunction: {}".format(self.name, self.column_name,
                                     self.number_of_positions,
                                     self.held_in_conjuction)

    def __repr__(self):
        return "Role({!r}, {!r}, {!r}, {!r})".format(self.name,
                                                     self.column_name,
                                                     self.held_in_conjuction,
                                                     self.number_of_positions)
