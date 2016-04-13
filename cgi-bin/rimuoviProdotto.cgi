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
my $descrizione = $cgi->param('descrizione');

# controllo se sto rimuovendo un fritto o una pizza
if($descrizione eq ''){ # voglio rimuovere una pizza
	# trovo il nodo
	my $pizza = $radice->findnodes("//pizza[\@nome='$nome']")->get_node(1);
	
	# mi sposto sul padre
	my $categoria = $pizza->parentNode;
	# elimino il figlio
	$categoria->removeChild($pizza);
}
else{	# voglio rimuovere un fritto
	chomp($descrizione);
	my $query = "//fritto[\@nome='$nome' and descrizione='$descrizione']";
	
	#my $temp = $radice->findnodes($query);
	my $fritto = $radice->findnodes($query)->get_node(1);
		
	# mi sposto sul padre
	my $categoria = $fritto->parentNode;
	# elimino il figlio
	$categoria->removeChild($fritto);
}

# serializzazione
open(OUT, ">$filedati") || die("Fallita apertura file");
print OUT $doc->toString  || die("Fallita scrittura file");
close(OUT);	

# torno al listino
my $url = "listinoAdmin.cgi";
print "Location: $url"."?=Elemento $nome rimosso\n\n";
	
exit;
