#!/usr/bin/perl -w

use XML::LibXML;
use HTML::Entities;
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

# print "Content-type: text/html\n\n";

my $cgi = new CGI;
my $filedati = "../data/listino.xml";
my $parser = XML::LibXML->new();	# crea il parser dell'XML
my $doc = $parser->parse_file($filedati) || die ("Errore nella parserizzazione del file xml");	# associa il parser all'XML
my $radice = $doc->getDocumentElement || die ("Errore nell'estrazione dell'elemento radice");		# individua la radice dell'XML

my $nome = $cgi->param('nome');
my $categoria = $cgi->param('categoria');
my $prezzo = $cgi->param('prezzoDaCambiare');

# creo la query adatta a seconda del tipo di prodotto di cui voglio cambiare il prezzo
$query;
if($categoria ne 'I Fritti'){ $query = "//pizza[\@nome='$nome']/prezzo/text()"; }
else{ $query = "//fritto[\@nome='$nome']/prezzo/text()"; }

# controllo il prezzo
if($prezzo !~ /^([\d]+)\.([\d]{2})$/){
	my $url = "listinoAdmin.cgi";
	print "Location: $url"."?=Formato prezzo inserito non valido\n\n";
	exit;
}

# trovo il nodo
my $prodotto = $radice->findnodes($query)->get_node(1);
$prodotto->setData($prezzo);	
	
# serializzazione
open(OUT, ">$filedati") || die("Fallita apertura file");
print OUT $doc->toString  || die("Fallita scrittura file");
close(OUT);	

# torno al listino
print $cgi->header(-location=>"listinoAdmin.cgi?msg=Prezzo cambiato con successo");
exit;