import Player

class GamePlayer(Player):
    def __init__(self, match):
        super().__init__(match)
        self.availableSoldiers = []
    def soldierArrange(self):
        if self.availableSoldiers == []:
            print("배치 가능한 병사가 없습니다.")
        else:
            print("배치 가능한 병사 리스트:\n", self.availableSoldiers)
            curSoldier = int(input("병사의 index를 입력하세요(1부터 시작): "))
            toGoal = int(input("목적지 골대번호를 입력하세요: "))
            self.availableSoldiers[curSoldier].move(toGoal)