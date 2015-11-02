console.log('Loading event');
var AWS = require('aws-sdk');
var dynamodb = new AWS.DynamoDB();

exports.handler = function(event, context) {
    console.log("Request received:\n", JSON.stringify(event));
    console.log("Context received:\n", JSON.stringify(context));

    var tableName = "AirportBaggage-Bags";

    dynamodb.scan({
            "TableName": tableName,
            "Select": "COUNT",
        }, function(err, data) {
            if (err) {
                context.fail('[ERROR] Query bag list: Dynamo failed: ' + err);
            } else {
                console.log('Dynamo Success: ' + JSON.stringify(data, null, '  '));
                context.succeed('{\"table_size\":' + '\"' + data.Count + '"}');
            }
        });
};
