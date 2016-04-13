#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use Switch;


my $cgi = new CGI;
my $file_xml = '../data/utenti.xml';
my $parser = XML::LibXML -> new();
my $doc = $parser->parse_file($file_xml) || die("Operazione di parsing fallita!");
my $radice = $doc->getDocumentElement ||die("Non si riesce ad accedere alla radice!");

# salvo i valori restituiti dal form in variabili
my $valore = $cgi->param('valore');		# è il valore del campo dati
my $voce = $cgi->param('voce');		# è la voce del profilo che si desidera modificare
my $username = $cgi->param('username');		# è lo username identificativo del profilo
my $conferma = $cgi->param('confermaPassword');	# questa variabile viene inizializzata solo se si cerca di cambiare la password

sub pulisci(){
	# pulisco la stringa passata da spazi all'inizio e alla fine e caratteri speciali
	$_[0] =~ s/^\s+|\s+$//g;
	$_[0] =~ s/</&lt;/g;
	$_[0] =~ s/>/&gt;/g;
	$_[0] =~ s/&/&amp;/g;
	$_[0] =~ s/'/&apos;/g;
	$_[0] =~ s/"/&quot;/g;
}

# applico la funzione creata ai valori recuperati dai campi dati del form
&pulisci($valore);
&pulisci($conferma);

# eseguo i controlli sulle voci sensibili
if($voce eq 'datanascita'){
	$valore =~ s/\//-/g; 
	my @dataScomposta = split(/-/,$valore);
	my $giorno = @dataScomposta[0];
	my $mese = @dataScomposta[1];
	my $anno = @dataScomposta[2];

	# controlli sulla data di nascita
	if($mese<1 || $mese>12){
		print $cgi->header(-location=>"gestisciProfilo.cgi?msg=Mese $mese inserito non valido");
		exit;
	}

	my $giornoMaxMese;

	use Switch;

	switch($mese){
	   case 1   { $giornoMaxMese = 31 }
	   case 2   { $giornoMaxMese = 29 }
	   case 3   { $giornoMaxMese = 31 }
	   case 4   { $giornoMaxMese = 30 }
	   case 5   { $giornoMaxMese = 31 }
	   case 6   { $giornoMaxMese = 30 }
	   case 7   { $giornoMaxMese = 31 }
	   case 8   { $giornoMaxMese = 31 }
	   case 9   { $giornoMaxMese = 30 }
	   case 10  { $giornoMaxMese = 31 }
	   case 11  { $giornoMaxMese = 30 }
	   case 12  { $giornoMaxMese = 31 }   
	}

	if($giorno < 1 || $giorno >$giornoMaxMese){
		print $cgi->header(-location=>"gestisciProfilo.cgi?msg=Giorno inserito non valido");
		exit;
	}

	# metto la data nel formato americano
	$valore = $anno.'-'.$mese.'-'.$giorno;
}

if($voce eq 'email'){ 
	# controllo la validità della mail
	if($valore !~ /^[\w\.\-]+@\w+[\w\.\-]*?\.\w{1,4}$/){
		print $cgi->header(-location=>"gestisciProfilo.cgi?msg=E-mail inserita non valida");
		exit;
	}
}


if($voce eq 'password'){ 
	# controlli sulla password
	if(length $valore > 16){
		print $cgi->header(-location=>"gestisciProfilo.cgi?msg=Lunghezza massima password 16 caratteri");
		exit;
	}

	if(length $valore < 6){
		print $cgi->header(-location=>"gestisciProfilo.cgi?msg=Lunghezza minima password 6 caratteri");
		exit;
	}

	if($valore ne $conferma){
		print $cgi->header(-location=>"gestisciProfilo.cgi?msg=Password non confermata");
		exit;
	}
}

# cerco l'elemento utente da modificare
my $query = "//utente[username='$username']/$voce/text()";
my $utente = $doc->findnodes($query)->get_node(1);

# modifico la voce
$utente->setData($valore);

# serializzo e chiudo
open(OUT, ">$file_xml");
print OUT $doc->toString;
close(OUT);

print $cgi->header(-location=>"gestisciProfilo.cgi?msg=voce $voce cambiata con successo");
exit;
