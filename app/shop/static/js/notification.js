const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notifications/' + USER_ID + '/'
);

chatSocket.onmessage = function(e) {
    console.log(e.data);
    //const data = JSON.parse(e.data);
};

chatSocket.onclose = function(e) {
    //console.error('Chat socket closed unexpectedly');
};
