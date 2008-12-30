<?php
class schem {
	var $CONVERT_PATH = "/usr/bin/convert";
	var $TMP_DIR = "/afs/csl.tjhsst.edu/students/2010/2010bhamrick/web-docs/tmp";
	var $CACHE_DIR = "/afs/csl.tjhsst.edu/students/2010/2010bhamrick/web-docs/cache";
	var $PREFIX = "/afs/csl.tjhsst.edu/students/2010/2010bhamrick/web-docs";
	var $WWW_PREFIX = "/~2010bhamrick";
	var $SCHEMATICS_DIR = "/afs/csl.tjhsst.edu/students/2010/2010bhamrick/web-docs/schematics";
	var $WWW_CACHE = "/~2010bhamrick/cache";
	
	function render_file($fname) {
		chdir($this->SCHEMATICS_DIR);
		$fin = fopen($this->PREFIX ."/". $fname, "r");
		$text = fread($fin,filesize($this->PREFIX."/".$fname));
		$tmpname = md5($text);
		if(!file_exists($this->CACHE_DIR . "/" . $tmpname . ".png")) {
			$command = "python ".$this->SCHEMATICS_DIR."/convert.py ".$this->PREFIX."/".$fname." ".$this->TMP_DIR."/".$tmpname.".eps";
			exec($command);
			$command = $this->CONVERT_PATH." ".$this->TMP_DIR."/".$tmpname.".eps ".$this->CACHE_DIR."/".$tmpname.".png";
			exec($command);
			unlink($this->TMP_DIR."/".$tmpname.".eps");
		}
		return "<img src=\"" . $this->WWW_CACHE . "/". $tmpname.".png". "\" />";
	}
}
?>
