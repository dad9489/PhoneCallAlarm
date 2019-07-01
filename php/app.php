<?php
/**
 * Copyright 2016 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

    use Silex\Application;
    use Symfony\Component\HttpFoundation\Request;
    use Symfony\Component\HttpFoundation\Response;
    use Symfony\Component\HttpFoundation\ParameterBag;
    use google\appengine\api\cloud_storage\CloudStorageTools;
    use Silex\Provider\TwigServiceProvider;
use Symfony\Component\Asset\Package;
use Symfony\Component\Asset\VersionStrategy\EmptyVersionStrategy;

$app = new Application();

/**
 * Routes:
 *
 * --------- GET ---------
 * /            serves homepage
 * /message     serves Twilio message to be read over phone, read from message.txt
 * /code        serves just the number code, read from code.txt
 * /alarm_bool  returns True or False signifying whether the alarm is currently going off, read from alarm_bool.txt
 * /beat_logs   returns string representation of list of beat logs
 * /alarm_times returns the contents of alarm_times.txt
 * /settings TODO serves HTML with diagnostic information including contents of beat_log.txt
 *
 * --------- POST ---------
 * /message     takes resp_message field of JSON content from request and saves to message.txt
 * /beat        saves JSON content from request to beat_log.txt, content includes fields device_name, time, alarm_bool
 *              responds with contents of alarm_times.txt
 * /alarm_times saves JSON conent from request to alarm_times.txt
 */

$app->before(function (Request $request) {
    if (0 === strpos($request->headers->get('Content-Type'), 'application/json')) {
        $data = json_decode($request->getContent(), true);
        $request->request->replace(is_array($data) ? $data : array());
    }
});

// register twig
$app->register(new TwigServiceProvider(), array(
    'twig.path' => __DIR__ . '/views',
    'twig.options' => array(
        'strict_variables' => false,
    ),
));

$app->get('/', function () use ($app) {
    $twig = $app['twig'];
    return $twig->render('index.html.twig'
//        ,array(
//        'books' => $bookList['books'],
//        'next_page_token' => $bookList['cursor'],)
    );
})->bind("homepage");

$app->get('/settings', function () use ($app) {
    $twig = $app['twig'];
    return $twig->render('settings.html.twig');
});

$app->get('/message', function () use ($app) {
    $my_bucket = CloudStorageTools::getDefaultGoogleStorageBucketName();
    $filename = "gs://$my_bucket/message.txt";
    $message = file_get_contents($filename);


    $response_text = new Twilio\TwiML\VoiceResponse();
    $response_text->say($message);

    $response = new Response((string) $response_text);
    $response->headers->set('Content-Type', 'text/xml');
    return $response;
});

$app->post('/message', function (Request $request) use ($app) {
    $post = array(
        'resp_message' => (string) $request->get('message'),
        'code' => (string) $request->get('code')
    );
    $my_bucket = CloudStorageTools::getDefaultGoogleStorageBucketName();
    $message_filename = "gs://$my_bucket/message.txt";
    $message_content = (string) $request->get('message');
    file_put_contents($message_filename, (string) $message_content);

    $code_filename = "gs://$my_bucket/code.txt";
    $code_content = (string) $request->get('code');
    file_put_contents($code_filename, (string) $code_content);

    return $app->json($post, 201);
});

$app->post('/message', function (Request $request) use ($app) {
    $post = array(
        'resp_message' => (string) $request->get('message')
    );
    $my_bucket = CloudStorageTools::getDefaultGoogleStorageBucketName();
    $filename = "gs://$my_bucket/message.txt";
    $content = (string) $request->get('message');
    file_put_contents($filename, (string) $content);


    return $app->json($post, 200);
});

$app->post('/beat', function (Request $request) use ($app) {
    $post = array(
        'device_name' => (string) $request->get('device_name'),
        'time' => (string) $request->get('time'),
        'alarm_bool' => (string) $request->get('alarm_bool')
    );
    $my_bucket = CloudStorageTools::getDefaultGoogleStorageBucketName();
    $filename = "gs://$my_bucket/beat_log.txt";
    $old_logs = (string) file_get_contents($filename);

    //only grab the $max_len most recent logs, old ones get lost
    $max_len = 49;  //the number of desired logs - 1
    $arr = explode("\n", $old_logs, $max_len+1);
    if(count($arr) > $max_len) {
        array_pop($arr);
    }
    $old_logs = implode("\n",$arr);

    $content = ((string) json_encode($post))."\n".$old_logs;
    $fp = fopen($filename, 'w');
    fwrite($fp, $content);
    fclose($fp);

    //save the contents of alarm_bool
    $alarm_bool_filename = "gs://$my_bucket/alarm_bool.txt";
    file_put_contents($alarm_bool_filename, (string) $request->get('alarm_bool'));

    $my_bucket = CloudStorageTools::getDefaultGoogleStorageBucketName();
    $filename = "gs://$my_bucket/alarm_times.txt";
    $alarm_times = file_get_contents($filename);
    return $alarm_times;
});

/**
 * Takes an element of an array and JSON decodes it. Used by array_walk to decode all elements of the beat_log
 * for GET /beat_log
 * @param $item a string representation of a a JSON object for beat data
 */
function parse(&$item) {
    $item = json_decode($item);
}

$app->get('/beat_logs', function () use ($app) {
    $my_bucket = CloudStorageTools::getDefaultGoogleStorageBucketName();
    $filename = "gs://$my_bucket/beat_log.txt";
    $old_logs = (string) file_get_contents($filename);
    $arr = explode("\n", $old_logs);
    array_walk($arr, 'parse');
    return json_encode($arr);
});

$app->get('/alarm_bool', function () use ($app) {
    $my_bucket = CloudStorageTools::getDefaultGoogleStorageBucketName();
    $filename = "gs://$my_bucket/alarm_bool.txt";
    $alarm_bool = file_get_contents($filename);
    return $alarm_bool;
});

$app->get('/code', function () use ($app) {
    $my_bucket = CloudStorageTools::getDefaultGoogleStorageBucketName();
    $filename = "gs://$my_bucket/code.txt";
    $code = file_get_contents($filename);
    return $code;
});

$app->get('/alarm_times', function () use ($app) {
    $my_bucket = CloudStorageTools::getDefaultGoogleStorageBucketName();
    $filename = "gs://$my_bucket/alarm_times.txt";
    $alarm_times = file_get_contents($filename);
    return $alarm_times;
});

$app->post('/alarm_times', function (Request $request) use ($app) {
    $post = array(
        'alarm_times' => (string) $request->get('alarm_times')
    );
    $my_bucket = CloudStorageTools::getDefaultGoogleStorageBucketName();
    $filename = "gs://$my_bucket/alarm_times.txt";
    $content = (string) $request->get('alarm_times');
    file_put_contents($filename, (string) $content);

    return $app->json($post, 200);
});

return $app;
