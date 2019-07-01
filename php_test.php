<!DOCTYPE html>
<html>
<head>
<title>Hello, World! Page</title>
</head>
<body>
<?php
	$post = array(
        'device_name' => 'test_device',
        'time' => '06:19',
        'alarm_bool' => 'True'
    );



	$old_logs = "{\"device_name\":\"test_device\",\"time\":\"06:18\",\"alarm_bool\":\"True\"}\n{\"device_name\":\"test_device\",\"time\":\"06:17\",\"alarm_bool\":\"True\"}\n{\"device_name\":\"test_device\",\"time\":\"06:16\",\"alarm_bool\":\"True\"}\n{\"device_name\":\"test_device\",\"time\":\"06:15\",\"alarm_bool\":\"True\"}\n{\"device_name\":\"test_device\",\"time\":\"06:14\",\"alarm_bool\":\"True\"}";
	$max_len = 4;
    $arr = explode("\n", $old_logs, $max_len+1);
	$last_element_split = explode("\n", end($arr));
	if(count($arr) > $max_len) {
		array_pop($arr);
	}
    $old_logs = implode("\n",$arr);
	
	$content = ((string) json_encode($post))."\n".$old_logs;
	echo $content;
?>
</body>
</html>