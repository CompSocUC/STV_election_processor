class STV:

    def __init__(self):
        self.members = set()
        self.votes = {}
        self.number_non_member_votes = 0
        self.roles = []


class Vote:

    def __init__(self, usercode):
        self.usercode = usercode


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
