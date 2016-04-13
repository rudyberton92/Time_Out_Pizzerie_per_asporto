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

# definisco una funzione per rimuovere spazi e caratteri speciali
sub pulisci(){
	# pulisco la stringa passata da spazi all'inizio e alla fine e caratteri speciali
	$_[0] =~ s/^\s+|\s+$//g;
	$_[0] =~ s/</&lt;/g;
	$_[0] =~ s/>/&gt;/g;
	$_[0] =~ s/&/&amp;/g;
	$_[0] =~ s/'/&apos;/g;
	$_[0] =~ s/"/&quot;/g;
}

# Ricevo dati POST
my $testo = $cgi->param('testo');
my $id = $cgi->param('id');
my $page = $cgi->param('page');

&pulisci($testo);

my $query = "//commento[ID='$id']/testo/text()";
my $commento = $doc->findnodes($query)->get_node(1);
$commento->setData($testo);

# serializzazione
open(OUT, ">$file_xml") || die("Fallita apertura file");
print OUT $doc->toString  || die("Fallita scrittura file");
close(OUT);	

if($page){
	print $cgi->header(-location=>"commentiAdmin.cgi?msg=Commento modificato con successo.");
}	
else{
	print $cgi->header(-location=>"commenti.cgi?msg=Commento modificato con successo.");
}

# Fine script
exit;
