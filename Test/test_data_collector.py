import unittest
import random
import copy


from main import *
from tools import generatorFileForTest, generatorDataForTest


class TestDataCollector(unittest.TestCase):
    
    def setUp(self):
        self.dataCollector = DataCollector()
        generatorFileForTest()
        self.infoFile = InformationFile(name_file="testData/testData.ods")

    def tearDown(self) -> None:
        os.remove("testData/testData.ods")

    def testFilterValidationData(self):
        arr = []
        for i in range(3):
            val = copy.copy(self.infoFile)
            val.raw_data = generatorDataForTest()
            val._dataValidation
            arr.append(val)
        self.assertTrue(len(self.dataCollector._filterValidData(arr)) == 3)

    def testFilterValidationDataOneBad(self):
        arr = []
        for i in range(3):
            val = copy.copy(self.infoFile)
            val.raw_data = generatorDataForTest()
            val._dataValidation
            arr.append(val)

        arr[2].status_validation = False
        self.assertTrue(len(self.dataCollector._filterValidData(arr)) == 2)

    def testGetListFilesDir(self):
        self.assertIsInstance(self.dataCollector._getListAbsolutePathFiles(), list)
        self.assertTrue(len(self.dataCollector._getListAbsolutePathFiles()) > 2)
        
    def testFilerListByMarkerTrue(self):
        arr = ["123.ods", "12/asd/asdas/asdas.ods", "211.txt"]
        self.assertTrue("123.ods" in self.dataCollector._filerListByMarker(arr))
        self.assertTrue("12/asd/asdas/asdas.ods" in self.dataCollector._filerListByMarker(arr))

    def testFilerListByMarkerFalse(self):
        arr = ["123.ods", "12/asd/asdas/asdas.ods", "211.txt"]
        self.assertFalse("211.txt" in self.dataCollector._filerListByMarker(arr))


class TestInformationFile(unittest.TestCase):

    def setUp(self) -> None:
        generatorFileForTest()
        self.infoFile = InformationFile(name_file="testData/testData.ods")

    def tearDown(self) -> None:
        os.remove("testData/testData.ods")

    def testInformationFileInit(self):
        self.assertIsInstance(self.infoFile.raw_data, tuple)

    def testValidatorTrue(self):
        self.assertTrue(self.infoFile.giveStatusValidation())
    
    def testValidatorFalse(self):
        self.infoFile.raw_data = [
            ("Категория", "текст"),
            ("Подразделение", 0),
            ("ст", 1),
        ]
        for _ in range(20):
            self.infoFile.raw_data.append(("st", random.randint(0, 20)))

        self.infoFile._dataValidation()
        self.assertFalse(self.infoFile.giveStatusValidation())


    def testExtractionHederTypes(self):
        self.assertTrue(isinstance(self.infoFile.categories,int))
        self.assertTrue(isinstance(self.infoFile.troop,str))

    def testExtractionHederValues(self):
        self.assertEqual(self.infoFile.categories, 0)
        self.assertEqual(self.infoFile.troop, "ЦО")

    def testExtractionIndexLen(self):
        self.assertEqual(len(self.infoFile.index), 20)

    def testExtractionValuesLen(self):
        self.assertEqual(len(self.infoFile.values), 20)


class TestValidator(unittest.TestCase):

    def setUp(self) -> None:
        self.validator = Validator()

    def testValidatorTrue(self):
        value = ["Количественные показатели", 1, "Цо"]
        for _ in range(20):
            value.append(random.randint(0, 20))
        self.assertTrue(self.validator.validation(value))

    def testValidatorFalse(self):
        value = ["Количественные показатели", 1, 2]
        for _ in range(20):
            value.append(random.randint(0, 20))
        self.assertFalse(self.validator.validation(value))

    def testValidatorRouteTrue(self):
        self.assertTrue(self.validator._validatorRout("123", "text"))
        self.assertTrue(self.validator._validatorRout(12, "stats"))

    def testValidatorRouteFalse(self):
        self.assertFalse(self.validator._validatorRout(123, "text"))
        self.assertFalse(self.validator._validatorRout("123", "stats"))

    def testIsIntegerTrue(self):
        self.assertTrue(self.validator._isIntegerInTheRange(1,  (0, 20)))

    def testIsIntegerFalse(self):
        self.assertFalse(self.validator._isIntegerInTheRange(0.5, (0, 20)))

    def testIntegerInRangeTrue(self):
        self.assertTrue(self.validator._isIntegerInTheRange(2, (0, 20)))

    def testIntegerInRangeFalse(self):
        self.assertFalse(self.validator._isIntegerInTheRange(200, (0, 20)))

    def testIsStringTrue(self):
        self.assertTrue(self.validator._isString("123"))

    def testIsStringFalse(self):
        self.assertFalse(self.validator._isString(123))

    def testCheckMaskMatchingTrue(self):
        self.assertTrue(self.validator._checkMaskMatching((range(23))))

    def testCheckMaskMatchingFalse(self):
        self.assertFalse(self.validator._checkMaskMatching((range(2))))
