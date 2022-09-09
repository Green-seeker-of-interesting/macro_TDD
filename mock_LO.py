import os
import logging as lg

import pandas as pd

lg.basicConfig(filename="python.log")


class ReportFile:

    # level 2

    def GetValue(self, file_name: str) -> tuple:
        try:
            return self.GetValueWorker(file_name=file_name)
        except FileNotFoundError as e:
            lg.error(
                f"Ошибка чтения данных. \n\t Файл - {file_name} не найдне \n\t {e}")

    def SetArray(self, sheet: str, arr: tuple):
        try:
            self.writeArray(sheet, arr)
        except Exception as e:
            lg.error(f"Ошибка записи данных. \n\t Лис - {sheet} \n\t {str(e)}")

    def GetPath(self) -> str:
        return os.getcwd()

    # level 3

    def GetValueWorker(self, file_name: str):
        df = pd.read_excel(file_name)
        return tuple(tuple(x) for x in df.values)

    def writeArray(self, sheet_name: str, arr: tuple):
        with open("sheets/" + sheet_name + ".txt", "w") as f:
            for row in arr:
                f.write(",".join(map(str, row)) + "\n")
