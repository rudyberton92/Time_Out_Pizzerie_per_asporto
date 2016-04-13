#!/usr/bin/perl -w
 
# Inclusione dei pacchetti necessari
use CGI;
use CGI qw(Link Title);
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI::Pretty;
use CGI::Session();
use XML::LibXML;
use HTML::Template;
use Encode;

my $cgi=new CGI;
my $file_xml='../data/commenti.xml';

my $parser=XML::LibXML -> new();
my $doc= $parser->parse_file($file_xml) || die("Operazione di parsing fallita!");
my $radice=$doc->getDocumentElement ||die("Non si riesce ad accedere alla radice!");

# Ricevo dati POST
my $ID = $cgi->param('id');
my $page = $cgi->param('page');

# Eliminazione di un commento
# trovo il nodo
my $commento = $radice->findnodes("//commento[ID='$ID']")->get_node(1);
	
# mi sposto sul padre
my $categoria = $commento->parentNode;
# elimino il figlio
$categoria->removeChild($commento);
	
# serializzazione
open(OUT, ">$file_xml") || die("Fallita apertura file");
print OUT $doc->toString  || die("Fallita scrittura file");
close(OUT);	

if($page){
	print $cgi->header(-location=>"commentiAdmin.cgi?msg=Commento rimosso con successo.");
}	
else{
	print $cgi->header(-location=>"commenti.cgi?msg=Commento rimosso con successo.");
}	

# Fine script
exit;
