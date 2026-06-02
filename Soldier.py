import Object

class Soldier(Object):
    def __init__(self, cooldown=0, usable=True, assignedGoal=None, match=None):
        super().__init__(usable)
        self.cooldown = cooldown
        self.assignedGoal = assignedGoal
        self.match = match

    def execute_queen_command(self):
        if self.usable:
            print(f"카드 병사가 여왕의 명령을 수행합니다! (복귀까지 남은 시간: {self.cooldown}초)")
            if self.assignedGoal is not None:
                print(f" -> 현재 소속: {self.assignedGoal.order}번 골대")
        else:
            print("현재 카드 병사를 사용할 수 없는 상태(usable=False)입니다.")

    def move(self, destination):
        if not self.usable:
            print("현재 카드 병사를 사용할 수 없는 상태(usable=False)입니다.")
            return
        self.assignedGoal = destination
        self.match.goalposts[destination].addSolider(self)