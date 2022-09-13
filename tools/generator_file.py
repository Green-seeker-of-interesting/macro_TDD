import random

import pandas as pd

def generatorFileForTest():
    main_mas = [
        ["Категория", 0],
        ["Подразделение", "ЦО"]
    ]

    for i in range(0,20):
        main_mas.append(["Показатель_" + str(i) , random.randint(0,20)])
    
    df = pd.DataFrame(main_mas, columns=["Статистический показатель", "Количественные показатели"])
    df = df.set_index("Статистический показатель")
    df.to_excel("testData/" + "testData" + ".ods" )



def generatorDataForTest() -> tuple:
    main_mas = [
        ["Статистический показатель", "Количественные показатели"],
        ["Категория", random.randint(0, 3)],
        ["Подразделение", random.choice(["ЦО", "ОТ", "КГ", "ПР"])]
    ]

    for i in range(0,20):
        main_mas.append(["Показатель_" + str(i) , random.randint(0,20)])

    return tuple(tuple(x) for x in main_mas)  



if __name__ == "__main__":
    # generatorFileForTest()
    print(generatorDataForTest())