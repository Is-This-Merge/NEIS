class Object:
    def __init__(self, usable=True):
        self.usable = usable


class Soldier(Object):
    def __init__(self, cooldown=0, usable=True, assignedGoal=None):
        super().__init__(usable)
        self.cooldown = cooldown
        self.assignedGoal = assignedGoal

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
        #destination번 골대를 임시로 goal이라 지칭하겠음
        goal.addSoldier(self)
        print(f"카드 병사가 {destination}번 골대를 구성하기 위해 {goal.location} 좌표로 이동 중입니다...")


class Goalpost(Object):
    def __init__(self, location=(0, 0), order=1, soldiers=None, usable=True):
        super().__init__(usable)
        self.location = location
        self.order = order
        self.soldiers = soldiers if soldiers is not None else []