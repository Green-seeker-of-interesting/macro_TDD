import logging as lg
import os
import shutil

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

    def __init__(self, name_file: str) -> None:
        self.name_file = name_file
        self._readFile()
        self._dataValidation()
        self._dataExtraction()

    def giveStatusValidation(self) -> bool:
        return self.status_validation

    def giveIndex(self) -> tuple:
        return self.index

    def giveValues(self) -> tuple:
        return self.values

    def _readFile(self):
        reFile = ReportFile()
        self.raw_data = reFile.GetValue(self.name_file)

    def _dataValidation(self):
        validator = Validator()
        self.status_validation = validator.validation(
            [(lambda x: x[1])(x) for x in self.raw_data])

    def _dataExtraction(self):
        self.categories = self.raw_data[1][1]
        self.troop = self.raw_data[2][1]
        self.index = tuple((lambda x: x[0])(item)
                           for item in self.raw_data[3:])
        self.values = tuple((lambda x: x[1])(item)
                            for item in self.raw_data[3:])


class DataCollector:

    def fullDataCollection(self) -> list:
        files = self._filerListByMarker(self._getListAbsolutePathFiles())
        return self._filterValidData([InformationFile(name) for name in files])

    def _filterValidData(self, arr: list) -> list:
        return [x for x in arr if x.giveStatusValidation()]

    def _getListAbsolutePathFiles(sef) -> list:
        path_to_dir =  ReportFile().GetPath()
        out = []
        # TODO - Переписать на модуль os.path.join()
        for file in os.listdir(path_to_dir + "/Данные/"):
            out.append(path_to_dir + "/Данные/" + file)
        return out
        
    def _filerListByMarker(self, arr:list) -> list:
        return list(filter(lambda x: x.endswith(".ods"),arr))


class FileShifter:
    
    @classmethod
    def shifting(cls, files:list):
        cls.creationFolder(files)
        cls._shifting(files)

    @classmethod
    def creationFolder(cls, files:list):
        for name in cls._creationPathForNewDir(files):
            cls._creationFolder(name)

    @classmethod
    def _shifting(cls ,files:list):
        for file in files:
            cls._shiftFile(file)

    @classmethod    
    def _shiftFile(cls,file:InformationFile):
        shutil.copy(file.name_file, cls._generatorPath(file), follow_symlinks=False)

    def _creationPathForNewDir(files:list) -> list:
        out = []
        out.append(os.path.join(ReportFile().GetPath(), "По категориям"))
        for name in set([x.categories for x in files]):
            out.append(os.path.join(out[0], str(name)))
        return out

    def _creationFolder(file_name):
        try:
            os.mkdir(file_name)
        except OSError as e:
            lg.info("Ошибка создния категории. Такая уже сущетвует")

    def _generatorPath(item:InformationFile)->str:
        work_path = ReportFile().GetPath()
        return os.path.join(work_path, "По категориям",str(item.categories), os.path.basename(item.name_file))




def START(args=None):
    try:
        infoFiles = DataCollector().fullDataCollection()
        FileShifter.shifting(infoFiles)
        pass
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    START()
