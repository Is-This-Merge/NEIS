from Object import Object

class Hedgehog(Object):
    def __init__(self, radius, color, location):
        super().__init__()

        # 위치
        self.location = location

        # 반지름
        self.radius=radius

        #색깔
        self.color=color

        # 속도
        self.velocity=(0,0)

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
            print("현재 둥근 정도:100/100")
        else:
            print("고슴도치가 10 만큼 더 둥글어졌습니다.")
            print(f"현재 둥근 정도:{self.__roundness}/100")

    # 털 눕히기
    def dullify(self):
        self.__sharpness -= 10

        if self.__sharpness < 0:
            self.__sharpness = 0
            print("고슴도치 털을 더 이상 눕힐 수 없습니다.")
            print("현재 뾰족한 정도:0/100")

        else: 
            print("고슴도치 털이 10 만큼 더 눕혀졌습니다.")
            print(f"현재 뾰족한 정도:{self.__sharpness}/100")


    # 도망가기
    def runaway(self):
        self.usuable=False