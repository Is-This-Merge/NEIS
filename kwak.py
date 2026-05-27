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

    def move(self):
        if not self.usable:
            print("현재 카드 병사가 지쳐서 이동할 수 없습니다 (usable=False).")
            return

        if self.assignedGoal is None:
            print("명령 대기 중: 아직 할당된 골대가 없어서 이동할 수 없습니다.")
            return

        goalpost_location = self.assignedGoal.location
        goalpost_order = self.assignedGoal.order
        
        print(f"카드 병사가 {goalpost_location}번 골대를 구성하기 위해 {goalpost_location} 좌표로 이동 중입니다...")


class Goalpost(Object):
    def __init__(self, location=(0, 0), order=1, soldiers=None, usable=True):
        super().__init__(usable)
        self.location = location
        self.order = order
        self.soldiers = soldiers if soldiers is not None else []