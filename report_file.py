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

    def SetArray(self, target: str, arr: tuple):
        self.calc.SetArray(target,value=arr)

    def GetPath(self) -> str:
        return self.FSO.GetParentFolderName(filename=self.ui.Documents()[0])

    def mesege(self, msg:str):
        self.svc.MsgBox(str(msg))