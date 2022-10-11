from backend.DBOperation import DBOperation
from frontend.GUI import GUI

def main():
    databaseData = DBOperation()
    userInterface = GUI(databaseData)
    userInterface.main()
main()
