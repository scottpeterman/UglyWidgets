// Declare global variable
var channel;
var handler;

// Function to initialize QWebChannel
function initializeQWebChannel(callback) {
    channel = new QWebChannel(qt.webChannelTransport, function (initializedChannel) {
        handler = initializedChannel.objects.handler;
        if (typeof handler == 'undefined') {
            console.log('Handler not found');
        } else {
            console.log('Handler attached:', handler);
            if (typeof callback === 'function') {
                callback(handler);
            }
        }
    });
}

// Function to call Python handler
function callPythonHandler() {
    if (!handler) {
        console.log('Handler not initialized');
        return;
    }

    console.log('initialized javascript to python handler');
<!--    handler.callFromJs('Initialize Event from JavaScript!');-->
}

// Usage:
initializeQWebChannel(function() {
    callPythonHandler();
});

