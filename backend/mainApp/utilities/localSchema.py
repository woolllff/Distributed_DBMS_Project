
import pymysql


class LocalSchema:
    def __init__(self, serverIP, serverPort, serverUser, serverUserPwd, dbName) -> None:
        self.schema = {}
        characterSet = "utf8mb4"
        cursorType = pymysql.cursors.DictCursor

        self.schema["serverIP"] = serverIP
        self.schema["serverPort"] = serverPort
        self.schema["serverUser"] = serverUser
        self.schema["serverUserPwd"] = serverUserPwd
        self.schema["characterSet"] = characterSet
        self.schema["cursorType"] = cursorType
        self.schema["dbName"] = dbName

        try:
            self.connect()
            self.cursorObject = self.mySQLConnection.cursor()

        except Exception as e:
            print("Exception occured:{}".format(e))

        self.makeSchema()
        # end init

    def makeSchema(self):
        # save tables
        self.schema["tables"] = {}

        # Fetch and print the meta-data of the table
        tableslist = self.execute_query("show tables")
        for t in tableslist:
            self.addTable(t)

        # print(tableslist)
        self.addPkey()
        self.addFkey()

        # end MakeSchema

    def addTable(self, table):
        # get the table name
        tableName = table["Tables_in_{}".format(self.schema["dbName"])]
        self.schema["tables"][tableName] = {}
        # print(tableName)

        # get all the columns of the table
        columns = self.execute_query("DESCRIBE {}".format(tableName))
        for c in columns:
            # print(c["Field"])
            self.schema["tables"][tableName][c["Field"]] = c

        # end addTable

    def addPkey(self):
        self.schema["pk"] = {}
        pkoutput = self.execute_query(
            " Select * from  INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE CONSTRAINT_SCHEMA = \"{}\" ".format(self.schema["dbName"]))
        for pk in pkoutput:
            if(pk["CONSTRAINT_NAME"] == "PRIMARY"):
                t = pk["TABLE_NAME"]
                # print(pk)
                if (t not in self.schema["pk"]):    
                    self.schema["pk"][t] = []
                self.schema["pk"][t].insert( pk["ORDINAL_POSITION"], pk["COLUMN_NAME"])

        #end add primary keys 

    def addFkey(self):
        self.schema["fk"] = {}
        fkoutput = self.execute_query(
            " Select * from  INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE CONSTRAINT_SCHEMA = \"{}\" ".format(self.schema["dbName"]))
        for fk in fkoutput:
            if(fk["REFERENCED_TABLE_NAME"] != None):
                t = (fk["TABLE_NAME"],fk["REFERENCED_TABLE_NAME"])
                fk_name = fk["CONSTRAINT_NAME"]
                if(t not in self.schema["fk"]):
                    self.schema["fk"][t] = {}
                if(fk_name not in self.schema["fk"][t]):
                    self.schema["fk"][t][fk_name] = []
                self.schema["fk"][t][fk_name].insert( fk["POSITION_IN_UNIQUE_CONSTRAINT"], (fk["COLUMN_NAME"],fk["REFERENCED_COLUMN_NAME"]))

        # end add fk 

    def connect(self):
        self.mySQLConnection = pymysql.connect(
            host=self.schema["serverIP"], port=self.schema["serverPort"] , user=self.schema["serverUser"], password=self.schema["serverUserPwd"], db=self.schema["dbName"], charset=self.schema["characterSet"], cursorclass=self.schema["cursorType"])

        # end connect

    def execute_query(self, q):
        try:
            self.cursorObject.execute(q)
            return self.cursorObject.fetchall()
        except Exception as e:
            print("Exception occured:{}".format(e))
        # end Execute Query

    def disconnect(self):
        try:
            self.mySQLConnection.close()
        except Exception as e:
            print("Exception occured:{}".format(e))

    def getLocalSchema(self):
        return self.schema
        pass

    def showSchema(self):
        print("Server IP = {}".format(self.schema["serverIP"]))
        print("Server User = {}".format(self.schema["serverUser"]))
        print("Server Password = {}".format(self.schema["serverUserPwd"]))
        print("database name = {}".format(self.schema["dbName"]))

        print(self.schema["tables"] ,"\n")
        # for table in self.schema["tables"]:
        #     print(table)
        #     for col in self.schema["tables"][table]:
        #         print("\t\t" + col)
        #         print("\t\t\t\t", self.schema["tables"][table][col])
        print(self.schema["fk"],"\n")
        # for fk in self.schema["fk"]:
        #     print(fk)
        #     print("\t\t",  self.schema["fk"][fk])
        print(self.schema["pk"],"\n")
        # for pk in self.schema["pk"]:
        #     print(pk)
        #     print("\t\t",  self.schema["pk"][pk])
        # return self.schema
        # end show

    def __del__(self):
        self.disconnect()

        pass


if __name__ == "__main__":
    serverIP = "127.0.0.1"
    serverUser = "root"
    serverUserPwd = "12345"
    dbName = "test2db"
    ls = LocalSchema(serverIP, serverUser, serverUserPwd, dbName)
    # print(ls.showSchema())

    # fkoutput = ls.execute_query(
    #     " Select * from  INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE CONSTRAINT_SCHEMA = \"{}\" ".format(dbName))

    # for i in fkoutput:
    #     print(i["REFERENCED_TABLE_SCHEMA"])
    #     print("\n")
