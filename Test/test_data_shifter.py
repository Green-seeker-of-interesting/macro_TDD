import unittest
import os


from main import *
from tools import generatorFileForTest


class TestDataShifter(unittest.TestCase):

    def setUp(self):
        generatorFileForTest()
        self.infoFile = InformationFile(name_file="testData/testData.ods")

    def tearDown(self) -> None:
        os.remove("testData/testData.ods")

    def testGeneratorPath(self):
        infoFiles = DataCollector().fullDataCollection()
        for item in FileShifter._creationPathForNewDir(infoFiles):
            self.assertTrue(os.path.isabs(item))         

    def testGeneratorPathInclude(self):
        self.assertTrue(str(self.infoFile.categories)
                        in FileShifter._generatorPath(self.infoFile))
        self.assertTrue(
            "По категориям" in FileShifter._generatorPath(self.infoFile))

    def testCreationFolder(self):
        infoFiles = DataCollector().fullDataCollection()
        FileShifter.creationFolder(infoFiles)
        for item in FileShifter._creationPathForNewDir(infoFiles):
            self.assertTrue(os.path.isdir(item))
        # clear
        for item in FileShifter._creationPathForNewDir(infoFiles)[::-1]:
           os.rmdir(item)