from Object import Object


class Soldier(Object):
    COOLDOWN_TURNS = 3

    def __init__(self, match, assignedGoal):
        super().__init__()
        self.match = match
        self.assignedGoal = assignedGoal
        self.leftTurn = -self.COOLDOWN_TURNS
        self.assign(assignedGoal)

    def update_cooldown(self, currentTurn):
        if not self.usable and currentTurn - self.leftTurn >= self.COOLDOWN_TURNS:
            self.usable = True

    def is_available(self, currentTurn):
        self.update_cooldown(currentTurn)
        return self.usable and self.assignedGoal is None

    def execute_queen_command(self):
        # 여왕 명령: 지키던 골대에서 이탈 → 쿨다운 동안 사용 불가
        if self.assignedGoal and self in self.assignedGoal.soldiers:
            self.assignedGoal.removeSoldier(self)
        self.leftTurn = self.match.currentTurn
        self.assignedGoal = None
        self.usable = False

    def assign(self, goalpost):
        if not self.usable:
            return False
        self.assignedGoal = goalpost
        goalpost.addSoldier(self)
        return True
