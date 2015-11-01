console.log('Loading event');
var AWS = require('aws-sdk');
var dynamodb = new AWS.DynamoDB();

exports.handler = function(event, context) {
    console.log("Request received:\n", JSON.stringify(event));
    console.log("Context received:\n", JSON.stringify(context));

    var tableName = "AirportBaggage-Bags";

    /* If no json was passed then return the total number of bags
     * (i.e. table size).
     */
    /* Check if a status has been provided if the location is sec. area 2,
     * as the application may be asking for the number of bags that have
     * failed the second check.
     */
     /* Otherwise just use what is below. */

    dynamodb.query({
            "TableName": tableName,
            "IndexName": "location-index",
            "KeyConditions": {
                "location": {
                    "ComparisonOperator": "EQ",
                    "AttributeValueList": [{"S": event.bag_location}]
                }
            },
            "Select": "COUNT" // ??????
        }, function(err, data) {
            if (err) {
                context.fail('[ERROR] Query bag list: Dynamo failed: ' + err);
            } else {
                console.log('Dynamo Success: ' + JSON.stringify(data, null, '  '));
                context.succeed('[SUCCESS] Query bag list');
            }
        });
}
