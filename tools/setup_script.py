import random

from faker import Faker
import pandas as pd

from generator_file import createDirIfNotExses


fake = Faker("ru_RU")


def createRandonFile():
    main_mas = [
        ["Категория", random.randint(0,3)],
        ["Подразделение", fake.city()]
    ]

    for i in range(0,20):
        main_mas.append(["Показатель_" + str(i) , random.randint(0,20)])


    df = pd.DataFrame(main_mas, columns=["Статистический показатель", "Количественные показатели"])
    df = df.set_index("Статистический показатель")
    df.to_excel("Данные/" + main_mas[1][1] + ".ods" )


if __name__ == "__main__":
    createDirIfNotExses("Данные")
    for i in range(100):
        createRandonFile()