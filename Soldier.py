from Object import Object


class Soldier(Object):
    COOLDOWN_TURNS = 3  # 여왕이 빼간 뒤 다시 배치 가능해지기까지의 턴 수

    def __init__(self, match=None, assignedGoal=None):
        super().__init__()
        self.match = match
        self.assignedGoal = assignedGoal
        self.leftTurn = -self.COOLDOWN_TURNS  # 처음엔 바로 배치 가능

    def update_cooldown(self, currentTurn):
        if not self.usable and currentTurn - self.leftTurn >= self.COOLDOWN_TURNS:
            self.usable = True

    def is_available(self, currentTurn):
        self.update_cooldown(currentTurn)
        return self.usable and self.assignedGoal is None

    def execute_queen_command(self):
        # 여왕 명령: 지키던 골대에서 이탈 → 쿨다운 동안 사용 불가
        if self.assignedGoal and self in self.assignedGoal.soldiers:
            self.assignedGoal.soldiers.remove(self)
        self.leftTurn = self.match.currentTurn
        self.assignedGoal = None
        self.usable = False

    def assign(self, goalpost):
        if not self.usable:
            return False
        self.assignedGoal = goalpost
        goalpost.addSoldier(self)
        return True
