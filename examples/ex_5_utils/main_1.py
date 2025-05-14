import sys
sys.path.append("./")

from src import utils



while True:
    if utils.wait(1, "1"):
        print("Прошло 1 секунда")
    if utils.wait(5, "5"):
        print("Прошло 5 секунд")
    