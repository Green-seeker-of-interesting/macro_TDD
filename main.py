import logging as lg
import os
import shutil
import typing as tp

from scriptforge import CreateScriptService
from mock_LO import ReportFile


class Validator:

    RANGE_INT_VALIDATION: tp.Tuple[int, int] = (0, 100)

    MAP_VALIDATION: tp.List[str] = [
        "text", "stats", "text",  # heder
        # 20 stats params
        "stats", "stats", "stats", "stats", "stats",
        "stats", "stats", "stats", "stats", "stats",
        "stats", "stats", "stats", "stats", "stats",
        "stats", "stats", "stats", "stats", "stats",
    ]

    def validation(self, arr: list) -> bool:
        try:
            flags: tp.List[bool] = []
            for i, item in enumerate(arr):
                flags.append(self._validatorRout(item, self.MAP_VALIDATION[i]))
            return all(flags)

        except Exception as e:
            lg.warning(e, exc_info=True)
            return False

    def _checkMaskMatching(self, arr: tp.Tuple[tuple]) -> bool:
        return len(arr) == len(self.MAP_VALIDATION)

    def _validatorRout(self, value: tp.Any, mask: str) -> bool:
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
        self.name_file: str = name_file
        self._readFile()
        if self._dataValidation():
            self._dataExtraction()

    def giveStatusValidation(self) -> bool:
        return self.status_validation

    def giveIndex(self) -> tp.Tuple[str]:
        return self.index

    def giveValues(self) -> tp.Tuple[int]:
        return self.values

    def _readFile(self):
        reFile = ReportFile()
        self.raw_data: tp.Tuple[tuple] = reFile.GetValue(self.name_file)

    def _dataValidation(self) -> bool:
        validator = Validator()
        self.status_validation: bool = validator.validation(
            [(lambda x: x[1])(x) for x in self.raw_data])
        return self.status_validation

    def _dataExtraction(self):
        # Доверяем индексам так как файл уже прощёл валидацию
        self.categories: int = self.raw_data[1][1]   # type: ignore
        self.troop: str = self.raw_data[2][1]    # type: ignore
        self.index: tp.Tuple[str] = tuple((lambda x: x[0])(item)
                                          for item in self.raw_data[3:])
        self.values: tp.Tuple[int] = tuple((lambda x: x[1])(item)
                                           for item in self.raw_data[3:])


class DataCollector:

    def fullDataCollection(self) -> tp.List[InformationFile]:
        files = self._filerListByMarker(self._getListAbsolutePathFiles())
        return self._filterValidData([InformationFile(name) for name in files])

    def _filterValidData(self, arr: tp.List[InformationFile]) -> tp.List[InformationFile]:
        return [x for x in arr if x.giveStatusValidation()]

    def _getListAbsolutePathFiles(self) -> tp.List[str]:
        path_to_dir = ReportFile().GetPath()
        out = []
        # TODO - Переписать на модуль os.path.join()
        for file in os.listdir(path_to_dir + "/Данные/"):
            out.append(path_to_dir + "/Данные/" + file)
        return out

    def _filerListByMarker(self, arr: tp.List[str]) -> tp.List[str]:
        return list(filter(lambda x: x.endswith(".ods"), arr))


class FileShifter:
    # TODO - переписать без методов класса они тут не нужны

    @classmethod
    def shifting(cls, files: tp.List[InformationFile]):
        cls.creationFolder(files)
        cls._shifting(files)

    @classmethod
    def creationFolder(cls, files: tp.List[InformationFile]):
        for name in cls._creationPathForNewDir(files):
            cls._creationFolder(name)

    @classmethod
    def _shifting(cls, files: tp.List[InformationFile]):
        for file in files:
            cls._shiftFile(file)

    @classmethod
    def _shiftFile(cls, file: InformationFile):
        shutil.copy(file.name_file, cls._generatorPath(
            file), follow_symlinks=False)

    @classmethod
    def _creationPathForNewDir(cls, files: list) -> list:
        out = []
        out.append(os.path.join(ReportFile().GetPath(), "По категориям"))
        for name in set([x.categories for x in files]):
            out.append(os.path.join(out[0], str(name)))
        return out

    @classmethod
    def _creationFolder(cls, file_name: str):
        try:
            os.mkdir(file_name)
        except OSError as e:
            lg.info("Ошибка создния категории. Такая уже сущетвует")

    @classmethod
    def _generatorPath(cls, item: InformationFile) -> str:
        work_path = ReportFile().GetPath()
        return os.path.join(work_path, "По категориям", str(item.categories), os.path.basename(item.name_file))


class Table:

    def __init__(self, arr: tp.List[InformationFile]) -> None:
        self.raw_data: tp.List[InformationFile] = arr
        self.name: str = str(self.raw_data[0].categories)
        self._columnsInit()
        self._indexInit()
        self._calculation()

    def getFullTableValue(self) -> tp.List[list]:
        return self._rating(self._createWideTable())

    def _columnsInit(self):
        # TODO - Нужна ли валидация списка параметров?
        self.columns: tp.Tuple[str] = self.raw_data[0].giveIndex()

    def _indexInit(self):
        self.index: tp.Tuple[str] = tuple(x.troop for x in self.raw_data)

    def _calculation(self):
        self._createStatMatrix()
        self._calculationStatsEstimate()
        self._сalculationFinalGrade()

    def _createStatMatrix(self):
        self.stats_matrix: tp.Tuple[tp.Tuple[int]] = tuple(
            x.giveValues() for x in self.raw_data)

    def _calculationStatsEstimate(self):
        out: tp.List[tuple] = []
        for i in range(len(self.columns)):
            out.append(self._calculationPositiveEstimate(
                self._giveSatatParams(i)))
        self.estimate_matrix = self._T(out)

    def _calculationPositiveEstimate(self, colums: tp.Tuple[int]) -> tp.Tuple[float]:
        maxSP: int = max(colums)
        minSP: int = min(colums)
        out: tp.List[float] = [
            ((x - minSP) / (maxSP - minSP)) * 100 for x in colums]
        return tuple(round(x, 2) for x in out)

    def _giveSatatParams(self, col: int) -> tp.Tuple[int]:
        out = []
        for i in range(len(self.index)):
            out.append(self.stats_matrix[i][col])
        return tuple(out)

    def _сalculationFinalGrade(self):
        self.final_grade: tp.Tuple[float] = tuple(round(sum(row) / len(row), 2)
                                                  for row in self.estimate_matrix)

    def _createWideTable(self) -> tp.List[list]:
        out: tp.List[list] = []
        for row in range(len(self.index)):
            out.append([])
            for col in range(len(self.columns)):
                out[row].append(self.stats_matrix[row][col])
                out[row].append(self.estimate_matrix[row][col])
            out[row].append(self.final_grade[row])
        return out

    def _rating(self, arr: tp.List[list]) -> tp.List[list]:
        sortArr = sorted(arr, key=lambda x: x[-1], reverse=True)
        for i in range(len(sortArr)):
            sortArr[i].append(i+1)
        return sortArr

    def _T(self, matrix: tp.List[tp.Tuple[float]]) -> tp.Tuple[tp.Tuple[float]]:
        return tuple(map(tuple, zip(*matrix)))


class TableCreator:

    def creatingTable(self, arr: tp.List[InformationFile]) -> tp.List[Table]:
        return [Table(x) for x in self._sortByCategory(arr)]

    def _sortByCategory(self, arr: tp.List[InformationFile]) -> tp.Tuple[tp.List[InformationFile]]:
        tables: tp.Dict[str, tp.List[InformationFile]] = dict()
        for item in arr:
            if str(item.categories) in tables.keys():
                tables[str(item.categories)].append(item)
            else:
                tables.update({str(item.categories): [item]})
        return tuple(tables[key] for key in tables.keys())


class TableRecordManager:

    def __init__(self):
        self.rFile = ReportFile()

    def recordTables(self, tables: tp.List[Table]):
        for table in tables:
            self.record(table)

    def record(self, table: Table):
        self._recordBody(table)
        self._recordIndex(table)
        self._recordHeder(table)

    def _recordHeder(self, table: Table):
        sp: tp.List[str] = []
        for i, _ in enumerate(table.columns):
            sp.append("СП " + str(i+1))
            sp.append("ОП " + str(i+1))

        self.rFile.SetLine(
            sheet=table.name,
            target="B2",
            arr=sp,
        )

        self.rFile.SetLine(
            sheet=table.name,
            target="B1",
            arr=table.columns,
            step=1,
        )

    def _recordIndex(self, table: Table):
        self.rFile.SetArray(
            sheet=table.name,
            target="A3",
            arr=table.index
        )

    def _recordBody(self, table: Table):
        self.rFile.SetArray(
            sheet=table.name,
            target="B3",
            arr=table.getFullTableValue()
        )


class Formater:

    def __init__(self) -> None:
        self.calc = CreateScriptService("Calc")
    
    def formaterManager(self, tables: tp.List[Table]) -> None:
        for table in tables:
            self.calc.Activate(table.name)
            self._coloringTable(table)
            # self._createChart(table)

    def _coloringTable(self, table: Table):
        self._hederArt(table)
        self._indexArt(table)
        self._columsArt(table)

    def _createChart(self, table: Table):
        target = "A1:A" + str(len(table.index) + 2)
        self.calc.CreateChart(
            chartname="tables",
            sheetname=table.name,
            range=self.calc.Offset(target, 0, (len(table.columns) * 2 ) + 2)
        )

    def _indexArt(self, table:Table):
        target = "A1:A" + str(len(table.index) + 2)
        self.calc.SetCellStyle(target, "hed_and_index")

    def _columsArt(self, table: Table):
        target = "B2:B" + str(len(table.index) + 2)
        for ind, _ in enumerate(table.columns):
            self.calc.SetCellStyle(self.calc.Offset(target, 0, ind*2), "col1")
            self.calc.SetCellStyle(self.calc.Offset(target, 0, (ind*2) + 1), "col2")

    def _hederArt(self, table: Table):
        target = "A1:" + self._getLastColumnName() + "1"
        self.calc.SetCellStyle(target, "hed_and_index")
    
    def _getLastColumnName(self) -> str:
        return self.calc.LastCell('*').split("$")[2]


def START(args=None):
    try:
        infoFiles = DataCollector().fullDataCollection()
        FileShifter.shifting(infoFiles)
        tables = TableCreator().creatingTable(infoFiles)
        TableRecordManager().recordTables(tables)
        Formater().formaterManager(tables)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    START()
