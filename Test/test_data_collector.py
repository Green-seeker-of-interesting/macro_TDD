import unittest

from main import *
from tools import generatorFileForTest


class TestDataCollector(unittest.TestCase):
    pass


class TestInformationFile(unittest.TestCase):

    def setUp(self) -> None:
        generatorFileForTest()
        # data = self.reportFile.GetValue("testData/testData.ods")
        self.infoFile = InformationFile(name_file="testData/testData.ods")

    def tearDown(self) -> None:
        os.remove("testData/testData.ods")

    def testInformationFileInit(self):
        self.assertIsInstance(self.infoFile.raw_data, tuple)

    @unittest.skip("Пока не нужен")
    def testValidatorTrue(self):
        self.assertTrue(self.infoFile.giveStatusValidation())

    @unittest.skip("Пока не нужен")
    def testValidatorFalse(self):
        self.infoFile.raw_data = (
            ("Категория", "текст"),
            ("Подразделение", 0),
            ("ст", 1),
        )
        self.infoFile._dataValidation()
        self.assertFalse(self.infoFile.giveStatusValidation())


class TestValidator(unittest.TestCase):

    def setUp(self) -> None:
        self.validator = Validator()

    #  TODO - Дописать проверку валидатора когда будет система разбора данных 
    @unittest.skip("Нет разбора данных")
    def testValidatorTrue(self):
        self.assertTrue()
    

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
