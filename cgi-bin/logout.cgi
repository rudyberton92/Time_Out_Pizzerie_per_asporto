#!/usr/bin/perl -w

# librerie utilizzate
use CGI;
use CGI::Session();
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Cookie;

my $cgi=new CGI;

my $sid = $cgi->cookie("CGISESSID") || undef;

if($sid) {
    $session = load CGI::Session("driver:File", $sid, {Directory=>'session'});
    $session->delete();
    $session->flush();
    $session->clear();
}

my $c = $cgi->cookie(-name    =>  'CGISESSID',
		                 -value   =>  '',
		                 -expires =>  '-1d'
    );

	print "Set-Cookie: ",$c->as_string,"\n";
	print $cgi->header(-location=>"home.cgi?mess=logged-out");

exit;
