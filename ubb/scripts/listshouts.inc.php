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

	extract($in, EXTR_OVERWRITE | EXTR_REFS); // quick and dirty fix - extract hash values as vars

    $shout = new ShoutList('text');
    $shouts =& $shout->readShouts($start);
    if ($format == 'json') {
	    header('Content-type: application/json; charset=utf-8');
        echo json_encode($shouts);
    } else {
	    header('Content-type: text/xml; charset=utf-8');
        echo $shout->createShoutXml($shouts);
    }

	return false;
}

class ShoutList {
    private $graemlin_html = array();
    private $graemlin_code = array();
    private $graemlin_type = '';

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
            SELECT	s.SHOUT_ID as id, s.USER_ID as user_id, u.USER_DISPLAY_NAME as username, s.SHOUT_TEXT as body, s.SHOUT_TIME as time
            FROM	{$config['TABLE_PREFIX']}SHOUT_BOX as s, {$config['TABLE_PREFIX']}USERS as u
            WHERE	u.USER_ID = s.USER_ID AND s.SHOUT_ID > ?
            ORDER BY s.SHOUT_ID ASC
            LIMIT	$shout_limit
        ";

        $sth = $dbh->do_placeholder_query($query, array($start),__LINE__,__FILE__);
        $shouts = array();
        while($shout = $dbh->fetch_array($sth, MYSQL_ASSOC)) {
            $shout['body'] = $this->replaceGraemlins(str_replace("&lt;br&gt;", "<br />", $shout['body']));
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
