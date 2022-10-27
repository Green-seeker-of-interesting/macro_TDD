from scriptforge import CreateScriptService


class ReportFile:

    def __init__(self) -> None:
        self.calc = CreateScriptService("Calc")
        self.ui = CreateScriptService("UI")

        self.FSO = CreateScriptService("FileSystem")
        self.FSO.FileNaming = "SYS"
        self.svc = CreateScriptService("Basic")

    def GetValue(self, file_name: str) -> tuple:
        self.calc.CopySheetFromFile(file_name, "Sheet1", "value")
        self.calc.Activate("value")
        out_array = self.calc.GetValue("~.*")
        self.calc.RemoveSheet("value")
        return out_array

    def SetArray(self, sheet: str, target: str, arr: tuple):
        if not sheet in self.calc.Sheets:
            self.calc.InsertSheet(sheet)
        self.calc.SetArray(".".join([sheet, target]), value=arr)

    def GetPath(self) -> str:
        return self.FSO.GetParentFolderName(filename=self.ui.Documents()[0])

    # некрасивая функция, слищком много входных параметров
    def SetLine(self, arr: list, sheet: str, target: str, step: int = 0) -> None:
        self.calc.Activate(sheet)
        for i, val in enumerate(arr):
            self.calc.SetValue(self.calc.Offset(
                target, 0, i*(step+1)), str(val))

    def mesege(self, msg: str):
        self.svc.MsgBox(str(msg))