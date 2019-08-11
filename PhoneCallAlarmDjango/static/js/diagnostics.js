(function() {
    function startup() {
        // To avoid No 'Access-Control-Allow-Origin' header error:
        $.ajaxPrefilter( function (options) {
            if (options.crossDomain && jQuery.support.cors) {
                var http = (window.location.protocol === 'http:' ? 'http:' : 'https:');
                options.url = http + '//cors-anywhere.herokuapp.com/' + options.url;
            }
        });
        $.get(
            '/settings/code',
            function (response) {
                $('#diagnostics-code').text('Most recent code: ' + response);
            });
        $.get(
            '/settings/alarm_ringing',
            function (response) {
                $('#diagnostics-alarm-ringing').text('Alarm ringing: ' + response);
            });
    }


    // Set up our event listener to run the startup process
    // once loading is complete.
    window.addEventListener('load', startup, false);
})();