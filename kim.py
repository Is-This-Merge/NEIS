class Hedgehog:
    def __init__(self, location):
        # 위치
        self.location = location

        # 속도
        self.velocity = 0

        # 운동 방향
        # self.motion.velocity = "stop"

        # 뾰족한 정도
        self.__sharpness = 50

        # 둥근 정도
        self.__roundness = 50

    # 둥글어지기
    def rounder(self):
        self.__roundness += 10

        if self.__roundness > 100:
            self.__roundness = 100
            print("고슴도치를 더 이상 둥글게 할 수 없습니다.")
            print("현재 둥근 정도:0")
        else:
            print("고슴도치가 더 둥글어졌습니다.")
            print(f"현재 둥근 정도:{self.__roundness}")

    # 털 눕히기
    def dullify(self):
        self.__sharpness -= 10

        if self.__sharpness < 0:
            self.__sharpness = 0
            print("고슴도치 털을 더 이상 눕힐 수 없습니다.")
            print("현재 뾰족한 정도:0")

        else: 
            print("고슴도치 털이 10만큼 눕혀졌습니다.")
            print(f"현재 뾰족한 정도:{self.__sharpness}")

    # 굴러가기
    def roll(self, distance):
        self.velocity = distance

        self.location += distance

        self.motion = "rolling"

        print(f"고슴도치가 {distance}만큼 굴러갔습니다.")
        print(f"현재 위치: {self.location}")


    # 도망가기
    def runaway(self):
        print("고슴도치가 달아났습니다.")



class Flamingo:
    def __init__(self, hp, maxDistance):
        # 체력
        self.hp = hp

        # 최대 공격 거리
        self.maxDistance = maxDistance

        # 뻣뻣한 정도
        self.__stiffness = 50

    # 고슴도치 치기
    def hit(self, hedgehog, power):
        # power가 최대 거리보다 크면 제한
        if power > self.maxDistance:
            power = self.maxDistance

        print("홍학이 고슴도치를 쳤습니다!")

        hedgehog.roll(power)

        # 홍학 체력 감소
        self.hp -= 5

        if self.hp < 0:
            self.hp = 0

    # 사용 당하기
    def used(self):
        self.__stiffness += 5

        print("홍학이 사용되어 더 뻣뻣해졌습니다.")