console.log('Loading event');
var AWS = require('aws-sdk');
var dynamodb = new AWS.DynamoDB();

exports.handler = function(event, context) {
    console.log("Request received:\n", JSON.stringify(event));
    console.log("Context received:\n", JSON.stringify(context));

    var tableName = "AirportBaggage-Bags";

    if (event.bag_status == "failed sec. scan 2") {
        var db_query = {
            "TableName": tableName,
            "IndexName": "status-index",
            "KeyConditions": {
                "status": {
                    "ComparisonOperator": "EQ",
                    "AttributeValueList": [{"S": event.bag_status}]
                }
            },
            "Select": "COUNT"
        };
    } else {
        var db_query = {
            "TableName": tableName,
            "IndexName": "location-index",
            "KeyConditions": {
                "location": {
                    "ComparisonOperator": "EQ",
                    "AttributeValueList": [{"S": event.bag_location}]
                }
            },
            "Select": "COUNT"
        };
    }

    dynamodb.query(db_query,
        function(err, data) {
            if (err) {
                context.fail('[ERROR] Query bag list: Dynamo failed: ' + err);
            } else {
                console.log('Dynamo Success: ' + JSON.stringify(data, null, '  '));
                context.succeed('{\"count\":' + '\"' + data.Count + '\"}');
            }
        });
};
