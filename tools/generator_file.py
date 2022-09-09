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