/* Set up AWS */
AWS.config.region = "us-west-2";
AWS.config.update({"accessKeyId":"AKIAITXVMEKOPSBPGRQQ",
    "secretAccessKey":"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"});
var sqs = new AWS.SQS({"apiVersion":'2012-11-05'});

/* When the page loads, grab any existing data */
get_total_bag_num();
get_loading_bag_num();
get_sec2_bag_num();
get_plane_bag_number();

/* Functions for receiving SQS messages */
function sqs_subscribe(){
    console.log("Subscribing to https://sqs.us-west-2.amazonaws.com/979829065790/AirBagInfoQueue");
    var params = {
        "QueueUrl": "https://sqs.us-west-2.amazonaws.com/979829065790/AirBagInfoQueue",
        "WaitTimeSeconds": 20
    };
    sqs.receiveMessage(params, function (err, data) {
        console.log("Waiting for messages...");
        if (err){
            console.log("Rcv msg err ", err);
            return
        } else {
            if (data.Messages.length != 0)
                process_data(data);
        }
        setTimeout(sqs_subscribe(), 0);
    });
}

function process_data(data) {
    var message = data.Messages[0];
    var message_body = JSON.parse(message.Body);

    console.log("Recieved messages: ", message_body.Message);


    var params = {
        "QueueUrl": "https://sqs.us-west-2.amazonaws.com/979829065790/AirBagInfoQueue",
        "ReceiptHandle": message.ReceiptHandle
    };

    sqs.deleteMessage(params, function (err, data) {
        if (err)
            console.log(err, err.stack);
        else
            console.log("Message deleted successfully.")
    });
}

/* Subscribe to SQS queue */
sqs_subscribe();
