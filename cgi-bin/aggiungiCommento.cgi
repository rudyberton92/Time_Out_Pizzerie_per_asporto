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

# salvo i campi del form in delle variabili
my $utente=$cgi->param('utente');
my $testo=$cgi->param('testo');
my $sede=$cgi->param('sede');
my $data = $cgi->param('adddate');
my $pagina = $cgi->param('pagina');

# applico la funzione creata ai valori recuperati dai campi dati del form
&pulisci($testo);

#/foo/bar[not(preceding-sibling::bar/@score >= @score) and not(following-sibling::bar/@score > @score)]/@score

# Cerco l'ID piu alto 
my $commento = $radice->findnodes("//commento[not(preceding-sibling::commento/ID >= ID) and not(following-sibling::commento/ID > ID) ]")->get_node(1);
my $ID = $commento->getElementsByTagName("ID");
my $sID = " ".$ID." ";
$sID++;

if(!$data){
	# creo la data
	$secondi = (localtime)[0];
	$minuti = (localtime)[1];
	$ora = (localtime)[2];
	$anno = 1900+(localtime)[5];
	$mese = (localtime)[4];
	$giorno = (localtime)[3];

	$data = $anno.'-'.$mese.'-'.$giorno.'T'.$ora.':'.$minuti.':'.$secondi;
}


# creo un nuovo commento da inserire nel file xml
my $nuovo_commento="\n\t<commento>
		<ID>".$sID."</ID>
		<utente>".$utente."</utente>
		<testo>".$testo."</testo>
		<sede>".$sede."</sede>
		<data>".$data."</data>
	</commento>\n";
				
my $frammento= $parser->parse_balanced_chunk($nuovo_commento) || die(" Nodo non ben formato!");
$radice->appendChild($frammento) || die("Errore nell'inserimento del nuovo nodo");

# serializzazione
open(OUT, ">$file_xml") || die("Fallita apertura file");
print OUT $doc->toString  || die("Fallita scrittura file");
close(OUT);	

print $cgi->header(-location=>"$pagina?msg=Commento inserito con successo.");

# Fine script
exit;
