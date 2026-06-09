from Object import Object


class Soldier(Object):
    # 여왕이 빼간 뒤 다시 배치 가능해지기까지 걸리는 턴 수
    COOLDOWN_TURNS = 3

    def __init__(self, cooldown=COOLDOWN_TURNS, usable=True, assignedGoal=None, match=None):
        super().__init__(usable)
        self.cooldown = cooldown
        self.assignedGoal = assignedGoal
        self.match = match
        # 여왕에게 빼앗긴 턴. 처음에는 충분히 과거로 두어 바로 available 상태가 되게 함
        self.leftTurn = -self.COOLDOWN_TURNS

    def is_available(self, currentTurn):
        # 어느 골대에도 배치되어 있지 않고, 쿨다운이 지난 병사만 배치 가능
        if self.assignedGoal is not None:
            return False
        return (currentTurn - self.leftTurn) >= self.COOLDOWN_TURNS

    def execute_queen_command(self):
        # 여왕의 명령: 현재 지키던 골대에서 이탈
        if self.assignedGoal is not None and self in self.assignedGoal.soldiers:
            self.assignedGoal.soldiers.remove(self)

        self.leftTurn = self.match.currentTurn
        self.assignedGoal = None

    def assign(self, goalpost):
        # 골대에 배치
        if not self.usable:
            print("현재 카드 병사를 사용할 수 없는 상태(usable=False)입니다.")
            return False

        self.assignedGoal = goalpost
        goalpost.addSoldier(self)
        return True
