console.log('Loading event');
var AWS = require('aws-sdk');
var dynamodb = new AWS.DynamoDB();

exports.handler = function(event, context) {
    console.log("Request received:\n", JSON.stringify(event));
    console.log("Context received:\n", JSON.stringify(context));

    var tableName = "AirportBaggage-Bags";
    var datetime = new Date().getTime().toString();
    
    dynamodb.updateItem({
            "TableName": tableName,
            "Key": {
                "id": {
                    "S": event.bag_id
                }
            },
            "AttributeUpdates": {
                "timedate": {
                    "Action": "PUT",
                    "Value": {"N": datetime}
                },
                "location": {
                    "Action": "PUT",
                    "Value": {"S": event.bag_location}
                },
                "status": {
                    "Action": "PUT",
                    "Value": {"S" : event.bag_status}
                }
            }
        }, function(err, data) {
            if (err) {
                context.fail('[ERROR] Update bag: Dynamo failed: ' + err);
            } else {
                console.log('Dynamo Success: ' + JSON.stringify(data, null, '  '));
                context.succeed('[SUCCESS] Update bag');
            }
        });
}
