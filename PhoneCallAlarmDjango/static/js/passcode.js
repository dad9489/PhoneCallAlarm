var code = null;
var input = '';
let DOMAIN = 'https://phone-call-alarm.appspot.com';

(function() {
    var test = 'test';

    function startup() {
        // To avoid No 'Access-Control-Allow-Origin' header error:
        $.ajaxPrefilter( function (options) {
            if (options.crossDomain && jQuery.support.cors) {
                var http = (window.location.protocol === 'http:' ? 'http:' : 'https:');
                options.url = http + '//cors-anywhere.herokuapp.com/' + options.url;
            }
        });

        $.get(
            DOMAIN+'/code',
            function (response) {
                code = response;
                console.log(code);
            });
    }


    // Set up our event listener to run the startup process
    // once loading is complete.
    window.addEventListener('load', startup, false);
})();

function checkCode() {
    if(input === code) {
        console.log('correct');
        $('body,html').addClass('green');

        $.post(DOMAIN+"/beat",
            {
                device_name: "Webpage Keypad",
                time: new Date().toLocaleString(),
                alarm_bool: "False"
            });
    } else {
        $('body,html').removeClass('green');
    }
}