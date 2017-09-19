class STV:

    def __init__(self):
        self.members = set()
        self.votes = {}
        self.number_non_member_votes = 0


class Vote:

    def __init__(self, usercode):
        self.usercode = usercode
