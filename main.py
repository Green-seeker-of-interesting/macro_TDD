import os

from mock_LO import ReportFile

def START(args=None):
    pass


if __name__ == "__main__":
    rp = ReportFile()
    my_data = rp.GetValue("Данные/г.Томск.ods")
    rp.SetArray('1' ,my_data)