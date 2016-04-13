#!/usr/bin/perl -w

# print "Content-type: text/html\n\n";

# librerie utilizzate
use CGI;
use CGI::Session();
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Cookie;
use XML::LibXML;

my $cgi = new CGI;
          
$username = $cgi->param('user');
$password = $cgi->param('pwd');
$page = $cgi->param('page');
#print $username;
#print $password;

my $filedati="../data/utenti.xml";
my $parser=XML::LibXML->new();	# crea il parser dell'XML
my $doc=$parser->parse_file($filedati) || die ("Errore nella parserizzazione del file xml");	# associa il parser all'XML
my $root=$doc->getDocumentElement || die ("Errore nell'estrazione dell'elemento radice");		# individua la radice dell'XML

# and password='$password'
my $query = "//utente[username='$username' and password='$password']";
my $risultato = ($doc->findnodes($query))[0];

# print "Risulato".$risultato;

if($risultato) {
	my $session = new CGI::Session("driver:File", undef, {Directory=>'session'});
	my $amministratore = ($risultato->findnodes('amministratore'))[0];

	my $amministratoretext = $amministratore->textContent;

	# getting the effective session id:
	my $CGISESSID = $session->id();
	$session->param('username', $username);
	$session->param('pwd', $password);
	$session->param('amministratore', $amministratoretext);
	$session->expire('+1h');
	$session->param("~logged-in",1);
	$session->flush();

	my $c = $cgi->cookie(-name    =>  'CGISESSID',
		                 -value   =>  $session->id,
		                 -expires =>  '+3M'
	);

	print "Set-Cookie: ",$c->as_string,"\n";
       # print $cgi->header(-cookie=>$c);
	if(defined($page)) {
	        print $cgi->header(-location=>"$page?mess=logged");
	} else {
        	print $cgi->header(-location=>"home.cgi?mess=logged");	
	}

} else {
	if(defined($page)) {
	        print $cgi->header(-location=>"$page?msgErrLogin=Errore di autenticazione");
	} else {
        	print $cgi->header(-location=>"home.cgi?msgErrLogin=Errore di autenticazione");	
	}
}

exit;



