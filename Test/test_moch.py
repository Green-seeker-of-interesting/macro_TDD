import unittest

from mock_LO import *
from tools import generatorFileForTest


class TestReportFile(unittest.TestCase):

    def setUp(self) -> None:
        self.reportFile = ReportFile()

    def testGetPath(self):
        self.assertIsInstance(self.reportFile.GetPath(), str)

    def testCorrectPath(self):
        self.assertTrue(os.path.isdir(self.reportFile.GetPath()))


class TestReportFileGetValue(unittest.TestCase):

    def setUp(self) -> None:
        self.reportFile = ReportFile()
        generatorFileForTest()

    def tearDown(self) -> None:
        os.remove("testData/testData.ods")

    def testReportTypes(self):
        value = self.reportFile.GetValue("testData/testData.ods")
        self.assertIsInstance(value, tuple)
        self.assertIsInstance(value[0], tuple)

    def testReportExept(self):
        self.assertRaises(FileNotFoundError,
                          self.reportFile.GetValue("testData/123.txt"))
