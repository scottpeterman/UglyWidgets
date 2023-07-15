// Declare global variable


// Function to initialize QWebChannel
function initializeQWebChannel() {
    channel = new QWebChannel(qt.webChannelTransport, function (initializedChannel) {
        console.log('QWebChannel initialized');
    });
    return channel;
}

// Function to call Python handler
function callPythonHandler(channel) {
    if (!channel) {
        console.log('QWebChannel not initialized');
        return;
    }

    var handler = channel.objects.handler;
    console.log('Handler:', handler);
    return handler;
}