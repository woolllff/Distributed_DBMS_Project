# import pymysql

from .localSchema import LocalSchema

class GlobalSchema:
    def __init__(self) -> None:
        # (A,B) : [D,S,C]
        self.paths = {}
        # A : [B,C,D]
        self.graph = {}
        self.fKeys = {}
        self.localSchemas = []
        self.interDBkeys = {}
        # end init 

    def addLocalSchema(self,ls,servIP,servUser,servPass,dbname):
        l = LocalSchema(servIP,servUser,servPass,dbname)

        self.localSchemas.append((ls,servIP,servUser,servPass,dbname))
        
        for t in l.schema["tables"]:
            self.add_table("{}.{}".format(l.schema["dbName"],t))

        for fk in l.schema["fk"]:
            t1 = "{}.{}".format(l.schema["dbName"],fk[0])
            t2 = "{}.{}".format(l.schema["dbName"],fk[1])
            c1 = []
            c2 = []
            for fkName in l.schema["fk"][fk]:
                for (col1,col2) in l.schema["fk"][fk][fkName]:
                    c1.append(col1)
                    c2.append(col2)
                self.make_connection(fkName, t1, t2, c1, c2) 

    def delete_localSchema(self,l):
        for t in self.graph:
            if(t[0] == l[4]):
                for d in self.graph[t]:
                    self.graph[d].remove(t)
                del(self.graph[t])
        
        for db in self.fKeys[l[4]]:
            del(self.fKeys[l[4]][db])
        del(self.fKeys[l[4]])
        


    def updateLocalSchema(self,ls,servIP,servUser,servPass,dbname):
        
        for i in self.localSchemas:
            if(i[0] == ls):
                self.localSchemas.remove(i)
        
        self.addLocalSchema(ls,servIP,servUser,servPass,dbname)



    def getSchema(self):
        # g = {}
        # for i in self.graph:
        #     g["{}.{}".format(i[0],i[1])] = []
        #     for j in self.graph[i]:
        #         g["{}.{}".format(i[0],i[1])].append("{}.{}".format(j[0],j[1])) 
        
        return {"graph": self.graph , "localSchemas" : self.localSchemas , "fKeys" : self.fKeys, "interDBkeys" : self.interDBkeys} 
        
    def showSchema(self):
        print(self.graph)
        print("\n\n")
        print(self.fKeys)
        print("\n\n")
        
    def updateSchema(self,schema):
        # g = {}
        # for i in schema["graph"]:
        #     d,t = i.split(".")
        #     g[(d,t)] = []
        #     for j in schema["graph"][i]:
        #         d2,t2 = j.split(".")
        #         g[(d,t)].append((d2,t2))

        self.graph = schema["graph"]
        self.localSchemas = schema["localSchemas"]
        self.fKeys = schema["fKeys"]
        self.interDBkeys = schema["interDBkeys"]

    def add_table(self, table):
        # t = "{}.{}".format(table[0],table[1])
        if(table not in self.graph):
            self.graph[table] = []

    def remove_connection(self, t1, t2):
        if(t1 in self.graph[t2]):
            self.graph[t2].remove(t1)
        if(t2 in self.graph[t1]):
            self.graph[t1].remove(t2)
        
        # this needs fkey update and interdb keys 
        pass

    def remove_table(self, table):
        if(table in self.graph):
            for t in self.graph[table]:
                self.remove_connection(table, t)
            del(self.graph[table])

    def add_fk(self, fkname, table1, table2, c1, c2):
        db1,t1 = table1.split(".")
        db2,t2 = table2.split(".")

        if(db1 not in self.fKeys):
            self.fKeys[db1] = {}
        if(db2 not in self.fKeys[db1]):
            self.fKeys[db1][db2] = {}
        if(fkname not in self.fKeys[db1][db2]):
            self.fKeys[db1][db2][fkname] = (fkname,table1,table2,c1,c2)
      
        if(db1 != db2):
            if(db1 not in self.interDBkeys):
                self.interDBkeys[db1] = {}
            if(db2 not in self.interDBkeys[db1]):
                self.interDBkeys[db1][db2] = {}
            if(fkname not in self.interDBkeys[db1][db2]):
                self.interDBkeys[db1][db2][fkname] = (fkname,table1,table2,c1,c2)
    
        


    def make_connection(self, fkname, t1, t2, c1, c2):
        self.add_table(t1)
        self.add_table(t2)
        self.graph[t1].append(t2)
        self.graph[t2].append(t1)

        self.add_fk(fkname, t1, t2, c1, c2)
        self.add_fk(fkname, t2, t1, c2, c1)


    def makeSuggestions(self):
        n = len(self.localSchemas)
        for i in range(n):
            for j in range(i,n):
                self.suggest(self.localSchemas[i],self.localSchemas[j])
        # end make suggestions 
    
    def suggest(self,l1,l2):
        for t1 in l1.schema["tables"]:
            for col1 in l1.schema["tabels"][t1]:
                for t2 in l2.schema["tables"]:
                    for col2 in l2.schema["tabels"][t2]:
                        self.compareCol(l1.schema["tables"][t1][col1], l2.schema["tables"][t2][col2])

        
        pass
        # end suggest 


    def compareCol(self,c1,c2):
        pass

        #end compare col 

    def generate_paths(self,start, goal): 
        explored = []
        paths = []
        # Queue for traversing the
        # graph in the BFS
        queue = [[start]]

        # If the desired node is
        # reached
        if start == goal:
            print("Same Node")
            return

        # Loop to traverse the graph
        # with the help of the queue
        while queue:
            path = queue.pop(0)
            node = path[-1]

            # Condition to check if the
            # current node is not visited
            neighbours = self.graph[node]

            # Loop to iterate over the
            # neighbours of the node
            for neighbour in neighbours:
                if neighbour not in explored:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)        
                    # Condition to check if the
                    # neighbour node is the goal
                    if neighbour == goal:
                        print("Shortest path = ", *new_path)
                        print("\n")
                        # return
                        paths.append(new_path)
            print("\n")
            # print(queue)
            explored.append(node)

        # Condition when the nodes
        # are not connected
        if(len(paths) == 0):
            print("So sorry, but a connecting"
                    "path doesn't exist :(")
        return paths 



    def generate_paths_2(self,start, goal, parents=[]): 
        paths = []
        explored = [*parents]
        explored.append(start)
        # If the desired node is
        # reached
        if start == goal:
            # print("Same Node")
            return [[goal]]

        neighbours = self.graph[start]

        # Loop to iterate over the
        # neighbours of the node
        for neighbour in neighbours:
            if(neighbour not in parents):
                paths = [ *paths , *self.generate_paths_2(neighbour ,goal ,explored) ] 

        for p in paths:
            p.insert(0,start)

        # print(paths,"\n")
        return paths 



# Driver Code
if __name__ == "__main__":
     
    # Graph using dictionaries
    # graph = {'A': ['B', 'E', 'C'],
    #         'B': ['A', 'D', 'E'],
    #         'C': ['A', 'F', 'G'],
    #         'D': ['B', 'E'],
    #         'E': ['A', 'B', 'D'],
    #         'F': ['C'],
    #         'G': ['C']}

    gs = GlobalSchema()

    serverIP = "127.0.0.1"
    serverUser = "root"
    serverUserPwd = "12345"

    ls1 = LocalSchema(serverIP, serverUser, serverUserPwd, "employee")
    # ls1.showSchema()
    
    ls2 = LocalSchema(serverIP, serverUser, serverUserPwd, "department")
    # ls2.showSchema()

    ls3 = LocalSchema(serverIP, serverUser, serverUserPwd, "project")
    # ls2.showSchema()


    gs.addLocalSchema(ls1)
    gs.addLocalSchema(ls2)
    gs.addLocalSchema(ls3)
    

    gs.make_connection(('employee', 'employee'),('department', 'department'))
    gs.make_connection(('projects', 'project'),('department', 'department'))
    gs.make_connection(('projects', 'works_on'),('employee', 'employee'))
    
    paths = gs.generate_paths_2(('employee', 'employee'),('projects', 'project'))
    for p in paths:
        print(p,"\n")
    # print(gs.graph,"\n")
    # print(gs.fkey,"\n")
    # print(gs.paths,"\n")
    
