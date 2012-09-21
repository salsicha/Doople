
# USAGE
# Functions declared here are called with getattr() on the Doople class namespace:
# getattr(Doople.doople, json["method"])(json["params"], SendRPC)
# Functions are passed whatever parameters were sent from the client, plus a callback function to send messages with
# Pass id number to send to a specific client, pass to "everyone" to message all clients


def chat(params, SendRPC):
    SendRPC("receive", params, "everyone")
    print('relaying message to all')
