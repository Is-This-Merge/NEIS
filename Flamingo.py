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
    def hit(self, hedgehog, strength, direction):

        current_x, current_y = hedgehog.location
        dir_x, dir_y = direction

        new_x = current_x + (dir_x * strength)
        new_y = current_y + (dir_y * strength)

        # 홍학 체력 감소
        self.hp -= 10

        if self.hp < 0:
            self.usuable=False