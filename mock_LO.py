import os
import logging as lg
import typing as tp

import pandas as pd

lg.basicConfig(filename="python.log")


class ReportFile:


    def GetValue(self, file_name: str) -> tp.Tuple[tuple]:  # type: ignore
        try:
            return self._getValueWorker(file_name=file_name)
        except FileNotFoundError as e:
            lg.warning(e, exc_info=True)

    def SetArray(self, sheet: str, target: str, arr: tp.List[list]):
        try:
            self._writeArray(target, arr)
        except Exception as e:
            lg.warning(e, exc_info=True)

    def GetPath(self) -> str:
        return os.getcwd()


    def SetLine(self, arr: list, sheet: str, target: str, step: int = 0) -> None:
        pass

    def _getValueWorker(self, file_name: str):
        df = pd.read_excel(file_name)
        arr = [("Статистический показатель", "Количественные показатели")]
        for i in df.values:
            arr.append(i)
        return tuple(tuple(x) for x in arr)

    def _writeArray(self, sheet_name: str, arr: tp.List[list]):
        with open("sheets/" + sheet_name + ".txt", "w") as f:
            for row in arr:
                f.write(",".join(map(str, row)) + "\n")
