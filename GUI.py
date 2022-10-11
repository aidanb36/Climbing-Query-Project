import sys
class GUI:
    dataCollect = []
    def __init__(self, databaseData):
        self.database = databaseData
        self.isLoad = False
    def main(self):
        while True:
            self.menu()
            userChoice = input("Please choose one above --> ")
            if(self.isLoad):
                if(userChoice == "query data"):
                    try:
                        answer = []
                        userData = input("Query start --> ")
                        dataget, targetAttr = self.handleInput(userData)
                        databaseData = self.database.queryData(dataget)
                        self.dataCollect.append(databaseData)     

                        #output for query here
                        #for how
                        if(len(self.dataCollect[0])==1):
                            if len(databaseData[0]) == 1:
                                for data in databaseData[0]:
                                    print(data)
                            else:
                                #location and mountainName
                                if targetAttr == 'location' or targetAttr == 'mountainName':
                                    for data in databaseData[0]:
                                        answer.append(data)
                                    print(answer[1])

                                #elevation and type
                                elif targetAttr=='elevation' or targetAttr == 'type':
                                    for data in databaseData[0]:
                                        answer.append(data)
                                    print(answer[2])

                                #rockType and grade
                                elif targetAttr =='rockType' or targetAttr == 'grade':
                                    for data in databaseData[0]:
                                        answer.append(data)
                                    print(answer[3])      
                                
                                #mountains and routes
                                elif targetAttr =='mountains' or targetAttr == 'routes':
                                    for data in databaseData[0]:
                                        answer.append(data)
                                    print(answer[0])      

                        #for join function    
                        else:
                            for data in self.dataCollect[0]:
                                answer.append(data)
                            for route in answer:
                                print(route[0])
                        self.dataCollect.clear()

                    #exception
                    except Exception as e:
                        print("Fetch data error, please try again")
                        print(e)
            else:
                if(userChoice == "load data"):
                    self.isLoad = True
                    self.database.loadData()
            if(userChoice == "help"):
                    self.help()
            elif(userChoice == "quit"):
                self.quit()

    def menu(self):
        menuText = ''
        if(self.isLoad):
            menuText = '''
                Welcome!
                Please enter one of the following commands:
                query data
                help
                quit
            '''
        else:
            menuText = '''
            Welcome to the mountains and climb data!
            For the first time, you need to load data.
            Please enter "load data" ( you dont need the quotes :) )
            You can also enter "help" for help with how to do queries
            or "quit" if you would like to quit the program
            
            Starter Commands:
            load data
            help
            quit
            '''
        print(menuText)

    def help(self):
        print('''
            Welcome to the mountains and climb data!
            For the first time, you need to load data.
            The tables and attributes you can query from are:
            mountains: (elevation,location,rockType)
            routes: (mountainName,type,grade)

            For querying data, there are a few kind of queries you can make:
            -for simple queries to find attributes for routes or mountains the format is "table key keyValue"
            (ex: "mountains elevation Bolton" or "routes grade Quartz Crack") 
            -to see how many mountains or routes there are the format is "how many table"
            (ex: how many mountains)
            -to see a list of the names for mountains or routes simply enter the table you would like to see
            -to see which routes are at a specific mountain the format 
            
            if you want to quit, just enter "quit"
            Thanks for using our mountains and climbs system
        
        ''')
    def handleInput(self, userInput):
        inputList = userInput.split()
        keyValue = " ".join(inputList[2:])
        #case for how many mountains or routes
        if inputList[0] == "how":
            return {"table": inputList[2], "key":'', "value": '', "count":True}, inputList[0]
        #case for list of mountains or routes 
        elif userInput=="mountains" or userInput=="routes":
             return {"table": inputList[0], "key":'', "value": '', "count":False}, inputList[0]
        #case for join commands (eg, routes mountain "~" or location route "~")
        elif inputList[1]=='route' or inputList[1]=='mountain':
            if inputList[1]=='route':
                return {"table": 'both', "key":'name', "value": keyValue, "count":False}, inputList[0]
            if inputList[1]=='mountain':
                return {"table": 'both', "key":'mountainName', "value": keyValue, "count":False}, inputList[0]
        #case for basic commands
        else:
            return {"table": inputList[0], "key":'name', "value": keyValue, "count":False}, inputList[1]
    def quit(self):
        sys.exit()
