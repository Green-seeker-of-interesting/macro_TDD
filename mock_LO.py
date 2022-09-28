import os
import logging as lg

import pandas as pd

lg.basicConfig(filename="python.log")


class ReportFile:

    # level 2

    def GetValue(self, file_name: str) -> tuple:
        try:
            return self._getValueWorker(file_name=file_name)
        except FileNotFoundError as e:
            lg.warning(e, exc_info=True)

    def SetArray(self, target: str, arr: tuple):
        try:
            self._writeArray(target, arr)
        except Exception as e:
            lg.warning(e, exc_info=True)

    def GetPath(self) -> str:
        return os.getcwd()

    # level 3

    def _getValueWorker(self, file_name: str):
        df = pd.read_excel(file_name)
        arr = [("Статистический показатель", "Количественные показатели")]
        for i in df.values:
            arr.append(i)
        return tuple(tuple(x) for x in arr)

    def _writeArray(self, sheet_name: str, arr: tuple):
        with open("sheets/" + sheet_name + ".txt", "w") as f:
            for row in arr:
                f.write(",".join(map(str, row)) + "\n")
