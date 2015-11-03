/* Get the current number of bags */
function get_total_bag_num() {
    var xhttp_bags = new XMLHttpRequest();
    xhttp_bags.onreadystatechange = function() {
        if (xhttp_bags.readyState == 4 && xhttp_bags.status == 200) {
            /* AWS API gateway does not play nice when it comes to
             * returning json, just read
             * https://blog.hiramsoftware.com/blog/day-one-aws-api-gateway/.
             * The solution below is ugly but it works.
             */
            var resp = JSON.parse(eval("["+xhttp_bags.responseText+"]")[0]);
            document.getElementById("total_bag_number").innerHTML = resp.table_size;
        }
    };
    xhttp_bags.open("GET", "https://kxy0yszwcb.execute-api.us-west-2.amazonaws.com/ver1/baggagetracking/system", true);
    xhttp_bags.send();
}

/* Get the current number of bags in security zone/area 2 */
function get_sec2_bag_num() {
    var xhttp_sec2 = new XMLHttpRequest();
    xhttp_sec2.onreadystatechange = function() {
        if (xhttp_sec2.readyState == 4 && xhttp_sec2.status == 200) {
            /* AWS API gateway does not play nice when it comes to
             * returning json, just read
             * https://blog.hiramsoftware.com/blog/day-one-aws-api-gateway/.
             * The solution below is ugly but it works.
             */
            var resp = JSON.parse(eval("["+xhttp_sec2.responseText+"]")[0]);
            document.getElementById("sec2_number").innerHTML = resp.Count;
        }
    };
    xhttp_sec2.open("GET", "https://kxy0yszwcb.execute-api.us-west-2.amazonaws.com/ver1/baggagetracking/sec-area-2", true);
    xhttp_sec2.send();
}

/* Get the current number of bags in the loading zone */
function get_loading_bag_num() {
    var xhttp_load = new XMLHttpRequest();
    xhttp_load.onreadystatechange = function() {
        if (xhttp_load.readyState == 4 && xhttp_load.status == 200) {
            /* AWS API gateway does not play nice when it comes to
             * returning json, just read
             * https://blog.hiramsoftware.com/blog/day-one-aws-api-gateway/.
             * The solution below is ugly but it works.
             */
            var resp = JSON.parse(eval("["+xhttp_load.responseText+"]")[0]);
            document.getElementById("loading_number").innerHTML = resp.Count;
        }
    };
    xhttp_load.open("GET", "https://kxy0yszwcb.execute-api.us-west-2.amazonaws.com/ver1/baggagetracking/loading-area", true);
    xhttp_load.send();
}

/* Get the current number of bags that have been dispatched to planes */
function get_plane_bag_number() {
    var xhttp_plane = new XMLHttpRequest();
    xhttp_plane.onreadystatechange = function() {
        if (xhttp_plane.readyState == 4 && xhttp_plane.status == 200) {
            /* AWS API gateway does not play nice when it comes to
             * returning json, just read
             * https://blog.hiramsoftware.com/blog/day-one-aws-api-gateway/.
             * The solution below is ugly but it works.
             */
            var resp = JSON.parse(eval("["+xhttp_plane.responseText+"]")[0]);
            document.getElementById("plane_number").innerHTML = resp.Count;
        }
    };
    xhttp_plane.open("GET", "https://kxy0yszwcb.execute-api.us-west-2.amazonaws.com/ver1/baggagetracking/plane", true);
    xhttp_plane.send();
}