function htmlDecode(input){
    var e = document.createElement('textarea');
    e.innerHTML = input;
    // handle case of empty input
    return e.childNodes.length === 0 ? "" : e.childNodes[0].nodeValue;
}

function insertNotification(data) {
    const li = document.createElement('li');
    li.className = 'notification';
    li.innerHTML = '' +
        '' + // icon here
        '<div class="information-box">' +
        '   <div class="notification-title">' +
        '       <p>' + data.title + '</p>' +
        '       <span class="notification-delete">Excluir</span>' +
        '   </div>' +
        '   <p class="notification-body">' + data.body + '</p>' +
        '   ' + // banner here
        '</div>';
    document.querySelector('ul.notification-list').prepend(li);
    const badge = document.createElement('span');
    badge.className = 'new badge';
    badge.setAttribute('data-badge-caption', '');
    badge.innerHTML = '1';
    document.getElementById('notification-dropdown-trigger').append(badge);
}

const notificationSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notifications/' + USER_ID + '/'
);
notificationSocket.onmessage = function(e) {
    const realData = JSON.parse(htmlDecode(e.data));
    if (realData.type === 'send_notification') {
        if (realData.data.pk) {
            const notify = document.querySelector('.notification[data-pk="' + realData.data.pk + '"]');
            if (notify) {
                notify.querySelector('.notification-title p').innerHTML = realData.data.title;
                notify.querySelector('p.notification-body').innerHTML = realData.data.body;
            } else {
                insertNotification(realData.data);
            }
        } else {
            insertNotification(realData.data);
        }
    }
    //const data = JSON.parse(e.data);
};
notificationSocket.onclose = function(e) {
    //console.error('Chat socket closed unexpectedly');
};
