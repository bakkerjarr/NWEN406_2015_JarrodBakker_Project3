console.log('Loading event');
var AWS = require('aws-sdk');
var dynamodb = new AWS.DynamoDB();

exports.handler = function(event, context) {
    console.log("Request received:\n", JSON.stringify(event));
    console.log("Context received:\n", JSON.stringify(context));

    var tableName = "AirportBaggage-Bags";
    var datetime = new Date().getTime().toString();
    
    dynamodb.putItem({
            "TableName": tableName,
            "Item": {
                "id": {
                    "S": event.bag_id
                }, 
                "timedate": {
                    "N": datetime
                },
                "location": {
                    "S": event.bag_location
                },
                "weight": {
                    "N": event.bag_weight
                },
                "status": {
                    "S" : event.bag_status
                }
            }
        }, function(err, data) {
            if (err) {
                context.fail('[ERROR] Create bag: Dynamo failed: ' + err);
            } else {
                console.log('Dynamo Success: ' + JSON.stringify(data, null, '  '));
                context.succeed('[SUCCESS] Create bag');
            }
        });
}
