import random
class fishing:
    def __init__(self,fish_list: list = []) -> None:
        self.fish_list = fish_list
        f = open('fish.txt','r',encoding="utf-8")
        for i in f.readlines():
            self.fish_list.append(i)
    def fishing(self) -> str:
        return random.choice(self.fish_list)

if __name__ == "__main__":
    print("OK")