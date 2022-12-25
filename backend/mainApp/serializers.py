from rest_framework import serializers
from .models import localSchemaModel, globalSchemaModel

from .utilities.globalSchema import GlobalSchema
from .utilities.localSchema import LocalSchema
import json


class localSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = localSchemaModel
        fields = "__all__"
        read_only_fields = ['schema']
    
    def create(self, data):
        ls = LocalSchema(data["serverIP"], data["serverPort"], data["serverUser"], data["serverPass"], data["dbName"])
        lsm = localSchemaModel.objects.create( 
            # **data,
            schemaName = data["schemaName"],
            serverIP = data["serverIP"],
            serverPort = data["serverPort"],
            serverPass = data["serverPass"],
            serverUser = data["serverUser"],
            dbName = data["dbName"],
            schema = "{}".format(ls.schema)
        )
        return lsm

    def update(self, instance, validated_data):
        # print("this is print validated data ",validated_data)
        data = {**validated_data}
        ls = LocalSchema(data["serverIP"], data["serverPort"], data["serverUser"], data["serverPass"], data["dbName"])
        data["schema"] = ls.getLocalSchema
        # print("this is the data generated for update ", data)
        return super().update(instance, data)



class globalSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = globalSchemaModel
        fields = "__all__"
        read_only_fields = ['schema']

    def create(self, data):
        gs = GlobalSchema()
        print("this is the data given to create ", data)
        
        for i in json.loads(data["localSchemas"])["ids"]:
            ls = localSchemaModel.objects.get(id = i)
            gs.addLocalSchema(i,ls.serverIP, ls.serverPort, ls.serverUser, ls.serverPass, ls.dbName)
            
        # print(json.loads("\"{}\"".format(gs.getSchema())))

        gsm = globalSchemaModel.objects.create(
            schemaName = data["schemaName"],
            schema = gs.getSchema(),
            localSchemas = data["localSchemas"]
        )
        return gsm

    def update(self, instance, validated_data):
        # print("this is print validated data ",validated_data)
        data = {**validated_data}
        gs = GlobalSchema()
        schema = instance.schema
        print(data)
        # print("this is the schema retrived from the db", schema)

        gs.updateSchema(schema)
        for i in json.loads(data["localSchemas"])["ids"]:
            ls = localSchemaModel.objects.get(id = i)
            gs.updateLocalSchema(i,ls.serverIP, ls.serverPort, ls.serverUser, ls.serverPass, ls.dbName)
        
        data["schema"] = gs.getSchema()
        # print("this is the data generated for update ", data)
        return super().update(instance, data)