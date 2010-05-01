<?php
//	Whoops!  If you see this text in your browser,
//	your web hosting provider has not installed PHP.
//
//	You will be unable to use UBB until PHP has been properly installed.
//
//	You may wish to ask your web hosting provider to install PHP.
//	Both Windows and Unix versions are available on the PHP website,
//	http://www.php.net/

if(!defined("UBB_MAIN_PROGRAM")) exit;
define('NO_WRAPPER',1);

function page_listshouts_gpc () {
	return array(
		"input" => array(
            "action" => array("action","get","string"),
            "secret" => array("secret","get","string"),
            "user_id" => array("user_id","get","string"),
            "user_name" => array("user_name","get","string"),
            "message" => array("message","get","string"),
			"start" => array("start","get","int"),
            "format" => array("format","get","string"),
		),
		"wordlets" => array(),
		"user_fields" => "",
		"regonly" => 0,
		"admin_only" => 0,
		"admin_or_mod" => 0,
		"no_session" => 1,
	);
} // end page_listshouts_gpc

function page_listshouts_run () {

	global $style_array,$smarty,$user,$in,$ubbt_lang,$config,$forumvisit,$visit,$dbh,$html;

    $shout = new ShoutList('text');
    $shout->dispatch($in);

	return false;
}

class ShoutList {
    private $graemlin_html = array();
    private $graemlin_code = array();
    private $graemlin_type = '';
    private $pass = 'u3nzcxvu8m34';
    private $max_word_len = 29;

    public function __construct($graemlin_type='') {
        global $dbh, $config, $html;

        $this->graemlin_type = $graemlin_type;

        // If we should show graemlins as text, we need info for the replacement.
        if ($this->graemlin_type == "text") {
            $img = '<img src="<<GRAEMLIN_URL>>/%s" alt="%s" title="%s" height="%s" width="%s" />';
            $html->get_graemlins();
            foreach($html->graemlins as $g) {
                list($code, $smiley, $image, $height, $width) = $g;
                $this->graemlin_html[] = sprintf($img, $image, $code, $code, $width, $height);
                $this->graemlin_code[] = $smiley ? $smiley : ":$code:";
            }
        }
    }

    public function dispatch($in) {
        if ($in['action'] == "send") {
            $this->sendShout($in);
        } else {
            $this->listShouts(intval($in['start']));
        }
    }

    private function getUserInfo($username) {
        global $config, $dbh;
        $query = "
            SELECT u.USER_ID, u.USER_DISPLAY_NAME 
            FROM   {$config['TABLE_PREFIX']}USERS u, {$config['TABLE_PREFIX']}USER_PROFILE p
            WHERE  u.USER_ID = p.USER_ID
            AND    p.USER_EXTRA_FIELD_1 = ?
            ORDER BY u.USER_ID ASC
            LIMIT 1
        ";
        $sth = $dbh->do_placeholder_query($query, array($username), __LINE__, __FILE__);
        while ($row = $dbh->fetch_array($sth)) {
            $user_id = $row[0];
            $user_name = $row[1];
        }
        if (!$user_id) {
            return false;
        }
        return array($user_id, $user_name);
    }

    private function parseMessage($text) {
        global $dbh, $config, $html, $ubbt_lang;

        // Long words should be wrapped in shoutbox messages.
        $text = htmlspecialchars(trim($text));
        $words = explode(" ", $text);
        foreach ($words as $i =>$w) {
            if (strlen(html_entity_decode($words[$i])) > $this->max_word_len) {
                $words[$i] = $html->utf8_wordwrap($words[$i], $this->max_word_len, "<br />", 1);
            } // end if
        } // end if
        $text = implode(" ", $words);

        // Handle markup code.
        $text = $html->do_markup($text,"shoutbox","markup");

        // Should text be censored?
        if ($config['DO_CENSOR']) {
            $text = $html->do_censor($text);
        }
        return $text;
    }

    public function sendShout($post) {
        global $dbh, $config, $html, $ubbt_lang;
        if ($post['secret'] != $this->pass) {
            echo "ERROR: INCORRECT PASSWORD";
        }

        // Get username and userid based on JID
        if (strpos($post['user_name'], '@') !== false) {
            if ($userinfo = $this->getUserInfo($post['user_name'])) {
                list($post['user_id'], $post['user_name']) = $userinfo;
            }
        }

        // user_id, user_name, message
        $query = "
            INSERT INTO {$config['TABLE_PREFIX']}SHOUT_BOX 
            (USER_ID, SHOUT_DISPLAY_NAME, SHOUT_TEXT, SHOUT_TIME, USER_IP) 
            VALUES (?, ?, ?, UNIX_TIMESTAMP(), '127.0.0.1')
        ";
        $username = $post['user_name'] ? $post['user_name'] : $ubbt_lang['ANON_TEXT'];
        $id = $post['user_id'] ? intval($post['user_id']) : 1;
        $post['message'] = $this->parseMessage($post['message']);
        $values = array($id, $username, $post['message']);
        $dbh->do_placeholder_query($query, $values, __LINE__, __FILE__);

        echo "OK";
    }

    public function listShouts($start) {
        $shouts =& $this->readShouts($start);
        if ($format == 'json') {
            header('Content-type: application/json; charset=utf-8');
            echo json_encode($shouts);
        } else {
            header('Content-type: text/xml; charset=utf-8');
            echo $this->createShoutXml($shouts);
        }
    }

    private function replaceGraemlins($str) {
        global $dbh, $config, $html, $style_array;

        if ($this->graemlin_type == "text") {
            $str = str_replace($this->graemlin_html, $this->graemlin_code, $str);
        } else {
            // Default to convert image URL
            $str = str_replace('<<GRAEMLIN_URL>>', "{$config['FULL_URL']}/images/{$style_array['graemlins']}", $str);
        }
        return $str;
    }

    public function readShouts($start=0) {
        global $dbh, $config, $html;

        $shout_limit = 30;
        $shouts = array();
        $query = "
            SELECT	s.SHOUT_ID as id, s.USER_ID as user_id, s.SHOUT_DISPLAY_NAME as username, s.SHOUT_TEXT as body, s.SHOUT_TIME as time
            FROM	{$config['TABLE_PREFIX']}SHOUT_BOX as s, {$config['TABLE_PREFIX']}USERS as u
            WHERE	u.USER_ID = s.USER_ID AND s.USER_IP <> '127.0.0.1' AND s.SHOUT_ID > ?
            ORDER BY s.SHOUT_ID ASC
            LIMIT	$shout_limit
        ";

        $sth = $dbh->do_placeholder_query($query, array($start),__LINE__,__FILE__);
        $shouts = array();
        while($shout = $dbh->fetch_array($sth, MYSQL_ASSOC)) {
            $shout['body'] = $this->replaceGraemlins(str_replace("&lt;br&gt;", "<br />", $shout['body']));
            $shout['body'] = preg_replace("#<a href='([^']*)' title='([^']*)' nofollow='nofollow' target='_blank'>\[LÄNK\]</a>#", "$2", $shout['body']);
            $shouts[] = $shout;
        } // end while

        return $shouts;
    }

    public function createShoutXml($data) {
        $doc = new DOMDocument('1.0', 'utf-8');
        $node = $doc->createElement("root");
        $rootnode = $doc->appendChild($node);
        $entries = array();
        foreach ($data as $row) {
            $body = $doc->createElement("body");
            $bodycontent = $doc->createCDATASection($row['body']);
            $body->appendChild($bodycontent);

            $node = $doc->createElement("message");
            $node->setAttribute('from', $row['username']);
            $node->setAttribute('from_id', $row['user_id']);
            $node->setAttribute('id', $row['id']);
            $node->setAttribute('time', $row['time']);
            $node->appendChild($body);

            $rootnode->appendChild($node);
        }
        return $doc->saveXML();
    }

}
