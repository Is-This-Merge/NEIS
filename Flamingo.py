from Object import Object

class Flamingo(Object):
    def __init__(self, maxDistance, stiffness):
        super().__init__()

        # 체력
        self.hp = 100

        # 최대 공격 거리
        self.maxDistance = maxDistance

        # 뻣뻣한 정도
        self.__stiffness = stiffness

    # 고슴도치 치기
    def hit(self, strength, direction):

        print("홍학이 고슴도치를 쳤습니다!")

        # 고슴고치 굴러 가야 하는데.........................................

        # 홍학 체력 감소
        self.hp -= 10

        if self.hp < 0:
            self.usualble=False