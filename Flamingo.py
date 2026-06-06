from Object import Object

class Flamingo(Object):
    match = None
    def __init__(self, match, maxDistance, stiffness):
        super().__init__()
        Flamingo.match = match

        # 체력
        self.hp = 100

        # 최대 공격 거리
        self.maxDistance = maxDistance

        # 뻣뻣한 정도
        self.__stiffness = stiffness

    # 고슴도치 치기
    def hit(self, hedgehog, strength):

        # 홍학 체력 감소
        self.hp -= hedgehog.sharpness * strength / 100 * (1 - self.__stiffness / 100)

        if self.hp < 0:
            self.usuable=False