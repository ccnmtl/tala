$(function() {
    var conn;
    var log = $("#log");

    var currentRefresh = 1000;
    var defaultRefresh = 1000;
    var maxRefresh = 1000 * 5 * 60; // 5 minutes

    var updateToken = function() {
        $.ajax({
            url: window.fresh_token_url,
            type: "get",
            dateType: 'json',
            error: function(evt) {
                setTimeout(updateToken, currentRefresh);
            },
            success: function(d) {
                window.token = d.token;
            }
        });
    };

    var requestFailed = function(evt) {
        // circuit breaker pattern for failed requests
        // to ease up on the server when it's having trouble
        updateToken();
        currentRefresh = 2 * currentRefresh; // double the refresh time
        if (currentRefresh > maxRefresh) {
            currentRefresh = maxRefresh;
        }
        appendLog($("<div class='alert'><b>Connection closed. trying again in " + currentRefresh/1000 + " seconds</b></div>"));
        setTimeout(connectSocket,currentRefresh);
    };

    var connectSocket = function() {
        conn = new WebSocket(window.websockets_base + "?token=" + window.token);
        conn.onclose = requestFailed;
        conn.onmessage = onMessage;
        conn.onopen = function (evt) {
            currentRefresh = defaultRefresh;
            appendLog($("<div class='alert alert-info'><b>Connected to server.</b></div>"));
        };
    };

    var onMessage = function (evt) {
        var envelope = JSON.parse(evt.data);
        var data = JSON.parse(envelope.content);

        var entry = $("<div/>");
        entry.addClass("row");
        var d = new Date();
        var hours = d.getHours();
        var minutes = d.getMinutes();

        if (minutes < 10) {
            minutes = "0" + minutes;
        }
        entry.append("<div class='span1 timestamp'>" + hours + ":" + minutes + "</div>");
        entry.append("<div class='span2 nick'>&lt;" + data.username + "&gt;</div>");
        entry.append("<div class='span5 ircmessage'>" + data.message_text + "</div>");
        appendLog(entry);
        MathJax.Hub.Queue(["Typeset",MathJax.Hub, entry]);
    };

    function appendLog(msg) {
        var d = log[0];
        var doScroll = d.scrollTop == d.scrollHeight - d.clientHeight;
        msg.appendTo(log);
        if (doScroll) {
            d.scrollTop = d.scrollHeight - d.clientHeight;
        }
    }


    $("#msg_form").submit(function() {
        var msg = $("#text-input");
        $.ajax({
            type: 'POST',
            url: "post/",
            data: {'text': msg.val()},
            success: function () {msg.val('');},
            error: function () { alert('post failed'); }
        });
        return false;
    });

    if (window.WebSocket) {
        connectSocket();
    } else {
        appendLog($("<div><b>Your browser does not support WebSockets.</b></div>"));
    }
});

