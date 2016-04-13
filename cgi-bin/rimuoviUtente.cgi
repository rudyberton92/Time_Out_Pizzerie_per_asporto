#!/usr/bin/perl -w

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

my $username = $cgi->param('username');
my $pagina = $cgi->param('pagina');

# cerco l'utente da rimuovere attraverso lo username passato come input nascosto
my $query = "//utente[username='$username']";
my $utenteDaRimuovere = $doc->findnodes($query)->get_node(1);

# mi sposto sul padre
my $padre = $utenteDaRimuovere->parentNode;

# elimino il figlio
$padre->removeChild($utenteDaRimuovere);

# serializzo e chiudo
open(OUT, ">$file_xml");
print OUT $doc->toString;
close(OUT);

if($pagina eq 'gestisciProfilo'){
	print $cgi->header(-location=>"logout.cgi");
}
else{
	print $cgi->header(-location=>"gestisciUtenti.cgi?msg=utente rimosso con successo");
}
exit;