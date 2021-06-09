const NotificationSystem = {
    htmlDecode: function(input){
        var e = document.createElement('textarea');
        e.innerHTML = input;
        // handle case of empty input
        return e.childNodes.length === 0 ? "" : e.childNodes[0].nodeValue;
    },
    deleteNotificationClick: function(e) {
        const notification = e.target.closest('.notification[data-pk]');
        const pk = parseInt(notification.getAttribute('data-pk'));
        const data = {
            type: 'delete_notification',
            data: {
                pk: pk,
            },
        };
        NotificationSystem.notificationSocket.send(JSON.stringify(data));
        const parent = notification.parentElement;
        parent.removeChild(notification);
        if (parent.childElementCount == 0) {
            parent.innerHTML = '<li class="notification-empty">Não há notificações para você!</li>';
        }
    },
    insertNotification: function(data) {
        const li = document.createElement('li');
        li.className = 'notification';
        li.setAttribute('data-pk', data.pk);
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
        const list = document.querySelector('ul.notification-list');
        const empty = list.querySelector('.notification-empty');
        if (empty !== null && empty !== undefined) {
            list.removeChild(empty);
        }
        list.prepend(li);
        li.querySelector('.notification-delete').addEventListener('click', NotificationSystem.deleteNotificationClick);
        const badge = document.createElement('span');
        badge.className = 'new badge';
        badge.setAttribute('data-badge-caption', '');
        badge.innerHTML = '1';
        document.getElementById('notification-dropdown-trigger').append(badge);
    },
    notificationSocket: new WebSocket(
        'ws://' + window.location.host + '/ws/notifications/' + USER_ID + '/'
    ),
    notificationReceiveMessage: function(e) {
        const realData = JSON.parse(NotificationSystem.htmlDecode(e.data));
        if (realData.type === 'send_notification') {
            if (realData.data.pk) {
                const notify = document.querySelector('.notification[data-pk="' + realData.data.pk + '"]');
                if (notify) {
                    notify.querySelector('.notification-title p').innerHTML = realData.data.title;
                    notify.querySelector('p.notification-body').innerHTML = realData.data.body;
                } else {
                    NotificationSystem.insertNotification(realData.data);
                }
            } else {
                NotificationSystem.insertNotification(realData.data);
            }
        }
    },
    start: function() {
        NotificationSystem.notificationSocket.onmessage = NotificationSystem.notificationReceiveMessage;
        const builtNotifications = document.querySelectorAll('.notification-list .notification-delete');
        Array.prototype.forEach.call(builtNotifications, function(item, index){
            item.addEventListener('click', NotificationSystem.deleteNotificationClick);
        });
    }
}

document.addEventListener('DOMContentLoaded', function(){
    NotificationSystem.start();
});
