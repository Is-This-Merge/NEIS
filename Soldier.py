from Object import Object

class Soldier(Object):
    def __init__(self, cooldown=2, usable=True, assignedGoal=None, match=None):
        super().__init__(usable)
        self.cooldown = cooldown
        self.assignedGoal = assignedGoal
        self.match = match
        self.leftTurn = 0

    def execute_queen_command(self):
        print(f"카드 병사가 여왕의 명령을 수행합니다! (복귀까지 남은 시간: {self.cooldown}턴)")
        self.leftTurn = self.match.currentTurn
        self.assignedGoal = None

    def move(self, destination):
        if not self.usable:
            print("현재 카드 병사를 사용할 수 없는 상태(usable=False)입니다.")
            return
        self.assignedGoal = destination
        self.match.goalposts[destination].addSoldier(self)