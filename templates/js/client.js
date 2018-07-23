$(document).ready(function() {

    //var socket = io.connect('http://' + document.domain + ':' + location.port);
    var socket = io.connect('127.0.0.1:5000');
    socket.on('connect', function() {
        socket.send('User has connected!')
    });
})