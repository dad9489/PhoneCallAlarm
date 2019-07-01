
let DOMAIN = 'https://phone-call-alarm.appspot.com';


$(document).ready(function(){
  $('.collapsible').collapsible();
  jQuery("time.timeago").timeago();

  $.get(
    DOMAIN+'/beat_logs',
    function (response) {
      var beat_logs = JSON.parse(response);

      //display beat logs from array
      $('#beat-collection').append('<ul class="collection"><br/>');
      for(i in beat_logs) {
        log = beat_logs[i];
        time_split = log.time.split(':');
        hours = parseInt(time_split[0].substring(time_split[0].length-2));
        minutes = parseInt(time_split[1].substring(0,2));
        time = twentyfour_to_twelve(hours, minutes);
        beat_html = '<li class="collection-item">'+'Device: '+log.device_name+' | Time: '+time+' | Alarm ringing: '+log.alarm_bool+'</li><br/>';
        $('#beat-collection').append(beat_html);
      }
      $('#beat-collection').append('</ul>');

      // most_recent_log = beat_logs[0];
      // time_split = most_recent_log.time.split(':');
      // hours = parseInt(time_split[0].substring(time_split[0].length-2));
      // minutes = parseInt(time_split[1].substring(0,2));
      // time = twentyfour_to_twelve(hours, minutes);
      $('#last-beat').text(jQuery.timeago(beat_logs[0].time));
  });
});