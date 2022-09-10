import logging as lg
import os

from mock_LO import ReportFile


class Validator:

    RANGE_INT_VALIDATION = (0, 100)

    MAP_VALIDATION = [
        "text", "stats", "text",  # heder
        # 20 stats params
        "stats", "stats", "stats", "stats", "stats",
        "stats", "stats", "stats", "stats", "stats",
        "stats", "stats", "stats", "stats", "stats",
        "stats", "stats", "stats", "stats", "stats",
    ]

    def validation(self, arr: list) -> bool:
        try:
            flags: list[bool] = []
            for i, item in enumerate(arr):
                flags.append(self._validatorRout(item, self.MAP_VALIDATION[i]))
            return all(flags)

        except Exception as e:
            lg.warning(e, exc_info=True)
            return False

    def _checkMaskMatching(self, arr: tuple) -> bool:
        return len(arr) == len(self.MAP_VALIDATION)

    def _validatorRout(self, value, mask: str) -> bool:
        if mask == "text":
            return self._isString(value)
        elif mask == "stats":
            return self._isIntegerInTheRange(value, self.RANGE_INT_VALIDATION)
        return False

    def _isIntegerInTheRange(self, value: int, rg: tuple) -> bool:
        return isinstance(value, int) and value >= rg[0] and value <= rg[1]

    def _isString(self, value: str) -> bool:
        return isinstance(value, str)


class InformationFile:

    # level 2

    def __init__(self, name_file: str) -> None:
        self.name_file = name_file
        self._readFile()
        self._dataExtraction()
        self._dataValidation()

    def giveStatusValidation(self) -> bool:
        pass

    def giveIndex(self):
        pass

    def giveValues(self):
        pass

    # level 3

    def _readFile(self):
        reFile = ReportFile()
        self.raw_data = reFile.GetValue(self.name_file)

    def _dataExtraction(self):
        pass

    def _dataValidation(self):
        # TODO - вставить сюда валидатор
        pass


class DataCollector:

    # level 1

    def fullDataCollection(self) -> list:
        pass

    # level 2

    def filterValidData(self):
        pass

    # level 3

    def _getListFilesOfDir(sef):
        pass


def START(args=None):
    try:
        pass
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    START()
