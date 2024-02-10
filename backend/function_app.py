import logging
import json
import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

#Bindings in declarative code(V2)
@app.route(route="CountTriggerFxn")
@app.cosmos_db_input(arg_name="inputDocument", 
                     database_name="cloudresumeDB",
                     container_name="counter",
                     #id="{Query.id}",
                     #partition_key="{id}",
                     sqlQuery = "SELECT * FROM c WHERE c.id = '1'",
                     connection="MyAccount_COSMOSDB")
@app.cosmos_db_output(arg_name="outputDocument", 
                      database_name="cloudresumeDB",
                      container_name="counter",
                      connection="MyAccount_COSMOSDB")

# HTTP Request
def GetCountValue(req: func.HttpRequest, inputDocument: func.DocumentList,
         outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    counter = getNewCounterValue(inputDocument[0]['count'])
    inputDocument[0]['count'] = counter
    outputDocument.set(func.Document.from_json(inputDocument[0].to_json()))

    if counter:
        return func.HttpResponse(
            body=json.dumps({
                "id": 1,
                "count": counter
            }),
            status_code=200,
            mimetype="application/json"
        )
    else:
        return func.HttpResponse(
            "Error",
            status_code=500
        )

def getNewCounterValue(value: int):
    return value + 1

