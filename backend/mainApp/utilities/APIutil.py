from .globalSchema import GlobalSchema
from .localSchema import LocalSchema


class APIutil:

    def __init__(self) -> None:
        self.lsl = []
        self.gs = GlobalSchema()


    def makeGS(self):
        self.gs = GlobalSchema()


    def makeLS(self , serIP, serUser, serPass, dbname):
        ls = LocalSchema(serIP,serUser,serPass,dbname)
        self.lsl.append(ls)

    def select_ls(self,lsl):
        i = 1
        print("\tEnter your choice")
        for ls in lsl:
            print("\t\t{}. {}".format(i, ls.schema["dbName"]))
            i += 1
        j = int(input("\t\t")) -1

        ls = lsl[j]
        return ls
    
    def select_table(self,ls):
        i = 1
        tables = []
        for table in ls.schema["tables"]:
            tables.append(table)
            print("\t\t\t{}. {}".format(i,table))
            i += 1
        j = int(input("\t\t\t")) -1
        t = tables[j]
        return t
    
    def select_col(self,ls,table):
        i = 1
        cols = []
        for col in ls.schema["tables"][table]:
            cols.append(col)
            print("\t\t\t{}. {}".format(i,col))
            i += 1
        c = input("\t\t\tEnter comma seprated ordered columns\t").split(",")
        t = []
        for i in c:
            t.append(cols[int(i) -1])
        print(t)
        return t


    def handle(self, choice):
        if(choice == 1):
            ip = input("\tEnter IP for DB \t")
            user = input("\tEnter server user \t")
            password = input("\tEnter server password \t")
            dbname = input("\tEnter the DB name \t")
            self.makeLS(ip,user,password,dbname)

        elif(choice == 2):
            ls = self.select_ls(self.lsl)
            print(ls.schema)
        
        elif(choice == 3):
            self.makeGS()
        
        elif(choice == 4):
            self.gs.addLocalSchema(self.select_ls(self.lsl))          

        elif(choice == 5):
            ls = self.select_ls(self.gs.localSchemas)
            
            pass

        elif(choice == 6):
            self.gs.showSchema()
        
        elif(choice == 7):
            print("\t\tSelect from")
            ls1 = self.select_ls(self.gs.localSchemas)
            db1 = ls1.schema["dbName"]
            t1 = self.select_table(ls1)
            c1 = self.select_col(ls1,t1)

            print("\t\tSelect from")
            ls2 = self.select_ls(self.gs.localSchemas)
            db2 = ls2.schema["dbName"]
            t2 = self.select_table(ls2)
            c2 = self.select_col(ls2,t2)

            fkname = input("\t\tEnter fk relation name \t")

            self.gs.make_connection(fkname, (db1,t1), (db2,t2), c1 , c2 )

        elif(choice == 8):
            pass

        elif(choice == 9):
            return 




if __name__ == "__main__":
    choice = 0
    commandLine = APIutil()
    while(choice != 9):
        print("Enter your choice:")
        print("1. Make Local Schema")
        print("2. Display Local Schema")
        print("3. Make Global Schema")
        print("4. Add Local Schema to global")
        print("5. Delete Local Schema from Global")
        print("6. Display Global Schema")
        print("7. Make Connections")
        print("8. Fire Query")
        print("9. Exit")
        choice = int(input())
        commandLine.handle(choice)

