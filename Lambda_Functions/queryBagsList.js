console.log('Loading event');
var AWS = require('aws-sdk');
var dynamodb = new AWS.DynamoDB();

exports.handler = function(event, context) {
    console.log("Request received:\n", JSON.stringify(event));
    console.log("Context received:\n", JSON.stringify(context));

    var tableName = "AirportBaggage-Bags";

    dynamodb.query({
            "TableName": tableName,
            "IndexName": "location-index",
            "KeyConditions": {
                "location": {
                    "ComparisonOperator": "EQ",
                    "AttributeValueList": [{"S": event.bag_location}]
                }
            },
            "Select": "SPECIFIC_ATTRIBUTES",
            "AttributesToGet": ["id", "location", "status"]
        }, function(err, data) {
            if (err) {
                context.fail('[ERROR] Query bag list: Dynamo failed: ' + err);
            } else {
                console.log('Dynamo Success: ' + JSON.stringify(data, null, '  '));
                context.succeed('[SUCCESS] Query bag list');
            }
        });
}
