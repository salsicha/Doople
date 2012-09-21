
// DEMO APP: chat

// USAGE
// To send a message to the server:
// SendRPC("methodname", ["param", "array"])
// To receive a message, make a function:
// function receive(name, message){
// And then send a message with method set as that function name from the server.
// Jquery 1.8 is already imported and available for use


// function receive(name, message) {
function receive(message) {
	console.log("received");
	$("#messages").append("<br>"+name+": "+message);
}

$("#send-message").click(function() {
	var method = "chat";
	var params = Array($("#text-input").val());
	console.log("sending message: " + $("#text-input").val());
	SendRPC(method, params);
});
