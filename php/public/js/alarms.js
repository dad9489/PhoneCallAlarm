
alarm_times = [];

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
days_to_ids = {"Monday": 'Mon', "Tuesday": 'Tue', "Wednesday": 'Wed', "Thursday": 'Thu', "Friday": 'Fri',
  "Saturday": 'Sat', "Sunday": 'Sun'};



function get_alarm_html(alarm) {
  id = alarm.id;
  alarm_html = '<!-- Begin One Alarm -->' +
      '    <div class="alarm" id="'+id+'-outer">' +
      '      <br/>' +
      '      <div class="inner" id="'+id+'-inner">' +
      '        <h2 id="'+id+'-time">8:00am</h2>' +
      '        <h4 id="'+id+'-days"></h4>' +
      '      </div>' +
      '      <div class="alarm-time-selection center-align">' +
      '        <div class="switch">' +
      '          <label style="color: lightgray">' +
      '            Off' +
      '            <input onclick="clicked(this)" type="checkbox" id="'+id+'-switch">' +
      '            <span class="lever"></span>' +
      '            On' +
      '          </label>' +
      '        </div> <br/>' +
      '        <a onclick="clicked(this)" class="waves-effect waves-light btn grey modal-trigger" href="#delete-modal" id="'+id+'-delete"><i class="material-icons">delete</i></a>' +
      '        <a onclick="clicked(this)" class="waves-effect waves-light btn grey modal-trigger" href="#edit-modal" id="'+id+'-edit"><i class="material-icons">edit</i></a>' +
      '      </div>' +
      '    </div>' +
      '<!-- End One Alarm -->';
  return alarm_html
}






/**
 * Initalizes the modals on the page.
 */
(function ($) {
  $(function () {
    //disable save
    $('#save').attr('disabled', true);
    $('#save').removeClass('pulse');
    function startup() {
      // To avoid No 'Access-Control-Allow-Origin' header error:
      $.ajaxPrefilter( function (options) {
        if (options.crossDomain && jQuery.support.cors) {
          var http = (window.location.protocol === 'http:' ? 'http:' : 'https:');
          options.url = http + '//cors-anywhere.herokuapp.com/' + options.url;
        }
      });

      $.get(
          DOMAIN+'/alarm_times',
          function (response) {
            alarm_times = JSON.parse(response);

            //display alarms from array
            $('#inner-alarm-time').empty();
            for(i in alarm_times) {
              alarm = alarm_times[i];
              alarm_html = get_alarm_html(alarm);
              $('#inner-alarm-time').append(alarm_html);
              update_page_by_alarm(alarm);
            }
          });
    }
    startup();

    //initialize all modals
    $('.modal').modal();

    $('#delete-modal').modal({
      startingTop: '30%',
      endingTop: '30%'
    });

    //or by click on trigger
    $('.trigger-modal').modal();

  }); // end of document ready
})(jQuery); // end of jQuery name space

/**
 * Preforms a variety of tasks depending on which of the buttons was clicked.
 * @param clicked_button the button that called this function. Needed so that the required behavior can be determined
 */
function clicked(clicked_button) {
  var id = clicked_button.id;
  var id_split = id.split('-');
  switch(id_split[1]) {
    case "edit":
      $('#confirm-edit').addClass(id_split[0]+'-alarmid');
      $('#edit-modal-title').text('Edit Alarm');
      $('#edit-submit').text('Continue');
      update_edit_by_alarm(get_alarm_by_id(id_split[0]));
      break;
    case "delete":
      $('#confirm-delete').addClass(id_split[0]+'-alarmid');
      break;
    case "switch":
      var on = $('#'+id).prop('checked');
      if(on) {
        $('#'+id_split[0]+'-inner').css("opacity", "1.0");
        get_alarm_by_id(id_split[0]).active = true;
      } else {
        $('#'+id_split[0]+'-inner').css("opacity", "0.5");
        get_alarm_by_id(id_split[0]).active = false;
      }
      $('#save').attr('disabled', false);
      $('#save').addClass('pulse');
      break;
  }
}

/**
 * Called when the add new alarm button is clicked. Creates a new alarm object and adds it to the alarm_times array,
 * then calls update_edit_by_alarm to update the elements of the page.
 */
function add_clicked() {

  $('#edit-modal-title').text('Add Alarm');
  $('#edit-submit').text('Add Alarm');

  var new_id = (Math.random()*0xFFFFFF<<0).toString(16);
  while(get_alarm_by_id(new_id)) {  // while there exists an item in the array with this id (generates unique id)
    new_id = (Math.random()*0xFFFFFF<<0).toString(16);
  }
  $('#confirm-edit').addClass(new_id+'-alarmid-new');
  new_alarm = {"id": new_id, "active": true, "days_active": ["Monday", "Tuesday", "Wednesday", "Thursday",
      "Friday", "Saturday", "Sunday"], "hour": 0, "minute": 0}
  alarm_times.push(new_alarm);
  update_edit_by_alarm(new_alarm);
}

/**
 * TODO
 */
function save_clicked() {
  $('#save').removeClass('pulse');
  $.post(DOMAIN+"/alarm_times",
      {
        alarm_times: JSON.stringify(alarm_times)
      }).done(function(msg){
        var toastHTML = '<span id="toast-container">' +
            '<h4>You have successfully saved your changes.<br/>Remember: changes can take up to 1 minute to take effect.</h4></span>';
        M.toast({html: toastHTML});
    $('#save').attr('disabled', true);
      }).fail(function(xhr, status, error) {
        var toastHTML = '<span id="toast-container" class="valign-wrapper">' +
            '<h4>An error occurred when attempting to submit data. <br/> Please try again.</h4></span>';
        M.toast({html: toastHTML});
        $('#save').addClass('pulse');
      });

}

function confirm_delete(modal_delete_button) {

  $('#save').attr('disabled', false);
  $('#save').addClass('pulse');
  //looks at the classlist, finds the class that was added by clicked(), gets the value of the id,
  //then removes the class
  class_list = Array.from(modal_delete_button.classList);
  var alarm_id = class_list.filter(obj => {
    var obj_split = obj.split('-');
    return obj_split[1] === 'alarmid'
  })[0].split('-')[0];
  $('#confirm-delete').removeClass(alarm_id+'-alarmid');

  alarm_times = alarm_times.filter(obj => {
    return obj !== get_alarm_by_id(alarm_id);
  });

  $('#'+alarm_id+'-outer').remove();
}

function confirm_edit(modal_edit_button) {
  $('#save').attr('disabled', false);
  $('#save').addClass('pulse');
  //looks at the classlist, finds the class that was added by clicked(), gets the value of the id,
  //then removes the class
  class_list = Array.from(modal_edit_button.classList);
  var alarm_id_split = class_list.filter(obj => {
    var obj_split = obj.split('-');
    return obj_split[1] === 'alarmid'
  })[0].split('-');
  alarm_id = alarm_id_split[0];
  $('#confirm-edit').removeClass(alarm_id_split.join('-'));
  var alarm = get_alarm_by_id(alarm_id);

  time_split = $('#edit-time').val().split(':');
  alarm.hour = parseInt(time_split[0]);
  alarm.minute = parseInt(time_split[1]);
  var days_active = []
  if($('#Mon').prop('checked')) {
    days_active.push("Monday")
  } if($('#Tue').prop('checked')) {
    days_active.push("Tuesday")
  } if($('#Wed').prop('checked')) {
    days_active.push("Wednesday")
  } if($('#Thu').prop('checked')) {
    days_active.push("Thursday")
  } if($('#Fri').prop('checked')) {
    days_active.push("Friday")
  } if($('#Sat').prop('checked')) {
    days_active.push("Saturday")
  } if($('#Sun').prop('checked')) {
    days_active.push("Sunday")
  }
  alarm.days_active = days_active;

  if(alarm_id_split.length === 3) {
    //this is a new alarm
    alarm_html = get_alarm_html(alarm);
    $('#inner-alarm-time').append(alarm_html);
    update_page_by_alarm(alarm);
  } else {
    //this is an edit to an existing alarm
    update_page_by_alarm(alarm);
  }
}

/**
 * Given an alarm javascript object, updates the edit modal to display the correct information about the alarm
 * @param alarm
 */
function update_edit_by_alarm(alarm) {
  $('#edit-time').val(time_convert(alarm.hour)+':'+time_convert(alarm.minute));
  not_active = arr_diff(days_of_week, alarm.days_active)
  // update checkboxes for days that are active
  for(i in alarm.days_active) {
    day_active = alarm.days_active[i];
    $('#'+days_to_ids[day_active]).prop('checked', true);
  }
  // update checkboxes for days that are not active
  for(i in not_active) {
    day_not_active = not_active[i];
    $('#'+days_to_ids[day_not_active]).prop('checked', false);
  }
}

function update_page_by_alarm(alarm) {
  id = alarm.id
  //update time
  $('#'+id+'-time').text(twentyfour_to_twelve(alarm.hour, alarm.minute));

  //update days
  var days_str = ''
  for(i in alarm.days_active) {
    if(i == 4) {
      days_str += '<br/>'
    }
    day_active = alarm.days_active[i];
    days_str += days_to_ids[day_active]+' '
  }
  $('#'+id+'-days').text('');

  if(days_str == '') {
    $('#'+id+'-days').text('(No days selected)');
  } else if(days_str == 'Mon Tue Wed Thu <br/>Fri Sat Sun ') {
    $('#'+id+'-days').text('Every day');
  } else if(days_str == 'Mon Tue Wed Thu <br/>Fri ') {
    $('#'+id+'-days').text('Weekdays');
  } else if(days_str == 'Sat Sun ') {
    $('#'+id+'-days').text('Weekends');
  } else {
    $('#'+id+'-days').append(days_str);
  }

  //update active
  if(alarm.active) {
    $('#'+id+'-inner').css("opacity", "1.0");
  } else {
    $('#'+id+'-inner').css("opacity", "0.5");
  }

  //update switch
  if(alarm.active) {
    $('#'+id+'-switch').prop('checked', true);
  } else {
    $('#'+id+'-switch').prop('checked', false);
  }
}

function twentyfour_to_twelve(hour, minute) {
  var time = ''
  if(hour - 12 > 0) {
    // 1:00PM to 11:00PM
    time = time_convert(hour-12)+':'+time_convert(minute)+'PM'
  } else if(hour == 12) {
    // 12:00PM
    time = time_convert(hour) + ':' + time_convert(minute) + 'PM'
  }
  else if(hour == 0) {
    time = time_convert(hour+12)+':'+time_convert(minute)+'AM'
  } else {
    // all other AM
    time = time_convert(hour)+':'+time_convert(minute)+'AM'
  }
  if(time[0] == '0') {
    time = time.substring(1)
  }
  return time
}


/**
 * Converts either an integer to a string representing an hour or minute, or a string to an int
 * Ex. 0 would return '00', '01' would return 1, '12' would return 12, etc.
 * @param time either a string or an int representing an hour or minute
 * @returns {string|string|*|number} either a string or an int, converted from the input
 */
function time_convert(time) {
  if(Number.isInteger(time)) {
    time_str = ''+time;
    if(time_str.length == 1) {
      return '0'+time_str;
    } else {
      return time_str;
    }
  } else {
    if(time[0] === '0') {
      return parseInt(time[1]);
    } else {
      return parseInt(time);
    }
  }
}

/**
 * Called by clear all in the edit modal, clears all checkboxes for the days
 */
function clear_all_checked() {
  $('#Sun').prop('checked', false);
  $('#Mon').prop('checked', false);
  $('#Tue').prop('checked', false);
  $('#Wed').prop('checked', false);
  $('#Thu').prop('checked', false);
  $('#Fri').prop('checked', false);
  $('#Sat').prop('checked', false);
}

/**
 * Called by select all in the edit modal, selects all checkboxes for the days
 */
function set_all_checked() {
  $('#Sun').prop('checked', true);
  $('#Mon').prop('checked', true);
  $('#Tue').prop('checked', true);
  $('#Wed').prop('checked', true);
  $('#Thu').prop('checked', true);
  $('#Fri').prop('checked', true);
  $('#Sat').prop('checked', true);
}

/**
 * Given an alarm javascript object, returns the value of its id
 * @param id the id of the given alarm object
 * @returns {null|T} either the string id value, or null if not found
 */
function get_alarm_by_id(id) {
  var result = alarm_times.filter(obj => {
    return obj.id === id
  })
  if (typeof result[0] === 'undefined') {
    return null
  }
  return result[0]
}

/**
 * Given two arrays, returns the difference, i.e. the values that are in one but not the other
 * @param a1 the first array
 * @param a2 the second array
 * @returns {Array} an array containing the difference
 */
function arr_diff (a1, a2) {

  var a = [], diff = [];

  for (var i = 0; i < a1.length; i++) {
    a[a1[i]] = true;
  }

  for (var i = 0; i < a2.length; i++) {
    if (a[a2[i]]) {
      delete a[a2[i]];
    } else {
      a[a2[i]] = true;
    }
  }

  for (var k in a) {
    diff.push(k);
  }

  return diff;
}
