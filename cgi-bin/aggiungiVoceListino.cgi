#!/usr/bin/perl -w

use XML::LibXML;
use HTML::Entities;
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use Encode;

#print "Content-type: text/html\n\n";

my $cgi = new CGI;
my $filedati = "../data/listino.xml";
my $parser = XML::LibXML->new();	# crea il parser dell'XML
my $doc = $parser->parse_file($filedati) || die ("Errore nella parserizzazione del file xml");	# associa il parser all'XML
my $radice = $doc->getDocumentElement || die ("Errore nell'estrazione dell'elemento radice");		# individua la radice dell'XML
my $temp = $radice->getElementsByTagName('categoria') || die "Errore nella creazione dell'array degli elementi 'categoria'";		# crea un array in cui mette tutti i commenti
my @categorie = $temp->get_nodelist();

# definisco una funzione per rimuovere spazi e caratteri speciali
sub pulisci(){
	$_[0] =~ s/^\s+|\s+$//g;
	$_[0] =~ s/[<]/[&lt;]/g;
	$_[0] =~ s/[>]/[&gt;]/g;
	$_[0] =~ s/[&]/[&amp;]/g;
	$_[0] =~ s/[']/[&apos;]/g;
	$_[0] =~ s/["]/[&quot;]/g;
}

my $nome = $cgi->param('nome');
my $prezzo = $cgi->param('prezzo');
my $categoriaParam = $cgi->param('categoria');
my $ingredienti = $cgi->param('ingredienti');
my $descrizione = $cgi->param('descrizione');

&pulisci($nome);
&pulisci($ingredienti);
&pulisci($descrizione);

if($categoriaParam eq ''){
	my $url = "listinoAdmin.cgi";
	print "Location: $url"."?msg=categoria non specificata\n\n";
	exit;
}

if($nome eq ''){
	my $url = "listinoAdmin.cgi";
	print "Location: $url"."?msg=Indicare un nome\n\n";
	exit;
}

if($prezzo !~ /^([\d]+)\.([\d]{2})$/){
	my $url = "listinoAdmin.cgi";
	print "Location: $url"."?=Il prezzo inserito non è valido\n\n";
	exit;
}

# eseguo un primo controllo sulla categoria di appartenenza del prodotto 
# prima di iniziare la procedura di inserimento
my $nuovoProdotto;
if($categoriaParam ne 'I Fritti' ){	# sto inserendo una pizza
	@ingredients = split(/, /,$ingredienti);
	# controllo che non ci siano virgole dovute ad un errato inserimento,
	# se ci sono le tolgo e preparo gli elementi <ingrediente>
	$nodiIngredienti = '';
	foreach $ingrediente(@ingredients){
		if($ingrediente =~ m/[,]/){
			$ingrediente =~ tr/[,]//;
		}
		$nodiIngredienti .= '<ingrediente>'.$ingrediente.'</ingrediente>'.'\n';
	}
	$nuovoProdotto = "\n<pizza nome=\"$nome\">
	 <prezzo valuta=\"euro\">$prezzo</prezzo>
	 <ingredienti>\n$nodiIngredienti\n</ingredienti>
	 </pizza>\n";
	
}
else{ #sto inserendo un fritto
	$nuovoProdotto = "\n<fritto nome=\"$nome\">
	 <prezzo valuta=\"euro\">$prezzo</prezzo>
	 <descrizione>$descrizione</descrizione>
	 </fritto>\n";
}
	 
my $puntoInnesto;
# cerco la categoria in cui inserire il nuovo elemento
foreach $nodoCategoria(@categorie){
	#$nodoCategoria = $categorie->get_node($c);	# nodoCategoria è un nodo elemento
	$nomeCategoria = $nodoCategoria->getAttribute("nome");
	if($nomeCategoria eq $categoriaParam){
		$puntoInnesto = $nodoCategoria;	
	}
}

# POST: a questo punto viene trovato il punto d'innesto. è di tipo Element

my $frammento = $parser->parse_balanced_chunk($nuovoProdotto) || die(" Nodo non ben formato!");

#$puntoInnesto->appendWellBalancedChunk($frammento) || die("Errore nell'inserimento del nuovo nodo");
$puntoInnesto->appendChild($frammento) || die("Errore nell'inserimento del nuovo nodo");

open(OUT, ">$filedati") || die("Fallita apertura file");
print OUT $doc->toString  || die("Fallita scrittura file");
close(OUT);	

print redirect(-url => "listinoAdmin.cgi?msg=Prodotto $nome inserito con successo");

exit;

