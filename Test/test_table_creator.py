import unittest


from main import *


class testTableCreator(unittest.TestCase):

    def setUp(self):
        self.tCreater = TableCreator()

    def testSortByCategory(self):
        infoFiles = DataCollector().fullDataCollection()
        for arr in self.tCreater._sortByCategory(infoFiles):
            flags = []
            for item in arr:
                flags.append(item.categories == arr[0].categories)
            self.assertTrue(all(flags))


class testTable(unittest.TestCase):

    def setUp(self) -> None:
        infoFiles = DataCollector().fullDataCollection()
        self.table = Table(TableCreator()._sortByCategory(infoFiles)[0])

    def testTableInit(self):
        self.assertIsInstance(self.table.raw_data, list)

    def testColumnsTable(self):
        self.assertIsInstance(self.table.columns, tuple)
        self.assertEqual(self.table.columns,
                         self.table.raw_data[3].giveIndex())

    def testIndexTableTypes(self):
        self.assertIsInstance(self.table.index, tuple)

    def testIndexTable(self):
        for item in self.table.raw_data:
            self.assertTrue(item.troop in self.table.index)

    def testCreateStatMatrix(self):
        self.assertEqual(len(self.table.stats_matrix), len(self.table.index))
        self.assertEqual(
            len(self.table.stats_matrix[0]), len(self.table.columns))

    def testCreateStatMatrixTypes(self):
        for row in self.table.stats_matrix:
            for item in row:
                self.assertIsInstance(item, int)

    def testGeiveStatsByIndex(self):
        self.assertEqual(len(self.table._giveSatatParams(0)),
                         len(self.table.index))

    def testcalculationPositiveEstimate(self):
        arr = tuple(range(20))
        cof = [0, 0.0526315789473684, 0.105263157894737, 0.157894736842105, 0.210526315789474,
               0.263157894736842, 0.31578947368421, 0.368421052631579, 0.421052631578947,
               0.473684210526316, 0.526315789473684, 0.578947368421053, 0.631578947368421,
               0.68421052631579, 0.736842105263158, 0.789473684210526, 0.842105263157895,
               0.894736842105263, 0.947368421052632, 1]

        out_value = self.table._calculationPositiveEstimate(arr)
        for i, val in enumerate(out_value):
            self.assertEqual(round(cof[i] * 100, 2), val)

    def testEstemateMatrixDimension(self):
        self.assertEqual(len(self.table.stats_matrix),
                         len(self.table.estimate_matrix))
        self.assertEqual(len(self.table.stats_matrix[0]), 
                         len(self.table.estimate_matrix[0]))

    def testEstemateMatrixRange(self):
        arr = tuple(map(tuple, zip(*self.table.estimate_matrix)))
        for row in arr:
            self.assertEqual(max(row), 100)
            self.assertEqual(min(row), 0)

    def testCalculationFinalGrade(self):
        self.assertEqual(len(self.table.final_grade), len(self.table.index))
        
    def testCreateWideTable(self):
        wideTabe = self.table.getFullTableValue()
        self.assertEqual(len(wideTabe[0]),
                         len(self.table.columns) * 2 + 2)
        self.assertEqual(len(wideTabe), 
                         len(self.table.index))

    def testRating(self):
        wideTabe = self.table.getFullTableValue()
        for i, item in enumerate(wideTabe[:-1]):
            self.assertTrue(item[-2] > wideTabe[i+1][-2] )