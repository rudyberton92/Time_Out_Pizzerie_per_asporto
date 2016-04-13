#!/usr/bin/perl -w

#print "Content-type: text/html\n\n";

# librerie utilizzate
use XML::LibXML;
use HTML::Entities;
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

my $cgi=new CGI;

my $file_xml="../data/utenti.xml";
my $parser=XML::LibXML->new();	# crea il parser dell'XML
my $doc=$parser->parse_file($file_xml) || die ("Errore nella parserizzazione del file xml");	# associa il parser all'XML
my $root=$doc->getDocumentElement || die ("Errore nell'estrazione dell'elemento radice");		# individua la radice dell'XML

my $accesso = $cgi->param('accesso');
my $username = $cgi->param('username');

# cerco la voce amministratore dell'utente da modificare
my $query = "//utente[username='$username']/amministratore/text()";
my $elementoAmministratore = $doc->findnodes($query)->get_node(1);

# modifico la voce
$elementoAmministratore->setData($accesso);

# serializzo e chiudo
open(OUT, ">$file_xml");
print OUT $doc->toString;
close(OUT);

print $cgi->header(-location=>"gestisciUtenti.cgi?msg=permessi cambiati con successo");
exit;