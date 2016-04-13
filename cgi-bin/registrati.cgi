#!/usr/bin/perl -w

# print "Content-type: text/html\n\n";	# per debug

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use XML::LibXML;
use Switch;
use Encode;


my $cgi=new CGI;
my $file_xml='../data/utenti.xml';
my $parser=XML::LibXML -> new();
my $documento= $parser->parse_file($file_xml) || die("Operazione di parsing fallita!");
my $radice=$documento->getDocumentElement ||die("Non si riesce ad accedere alla radice!");

#verifica del nome dell'elemento radice
#$elemento_radice = $radice -> getName() || die("La radice nn ha un nome");
#print $elemento_radice; 

# definisco una funzione per rimuovere spazi e caratteri speciali
sub pulisci(){
	$_[0] =~ s/^\s+|\s+$//g;
	$_[0] =~ s/</&lt;/g;
	$_[0] =~ s/>/&gt;/g;
	$_[0] =~ s/&/&amp;/g;
	$_[0] =~ s/'/&apos;/g;
	$_[0] =~ s/"/&quot;/g;
}

# salvo i campi del form in delle variabili
my $nome = $cgi->param('nome');
my $cognome = $cgi->param('cognome');
my $username = $cgi->param('username');
my $giorno = $cgi->param('giorno');
my $mese = $cgi->param('mese');
my $anno = $cgi->param('anno');
my $email = $cgi->param('email');
my $citta = $cgi->param('citta');
my $prefisso = $cgi->param('prefisso');
my $numero = $cgi->param('numero');
my $password=$cgi->param('password');
my $confPassword=$cgi->param('conf_password');

# applico la funzione creata ai valori recuperati dai campi dati del form
&pulisci($nome);
&pulisci($cognome);
&pulisci($username);
&pulisci($giorno);
&pulisci($mese);
&pulisci($anno);
&pulisci($email);
&pulisci($prefisso);
&pulisci($numero);
&pulisci($password);
&pulisci($confPassword);
&pulisci($citta);

# converto il formato di stampa da latin1 a utf8 per rendere i contenuti accettabili dalla funzione parse_balanced_chunk
Encode::from_to($nome,"latin1","utf8");
Encode::from_to($cognome,"latin1","utf8");
Encode::from_to($username,"latin1","utf8");
Encode::from_to($citta,"latin1","utf8");
Encode::from_to($password,"latin1","utf8");
Encode::from_to($confPassword,"latin1","utf8");

# Definisco la variabile msg che, alla fine di tutti i controlli, riporterà un messaggio di aiuto per la compilazione del form
my $msg = '';

# controlli sulla data di nascita, se presente
if($giorno ne '' && $mese ne '' && $anno ne ''){
	if($mese<1 || $mese>12){
		$msg .= 'Inserire un mese valido';
	}
	else{
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
			if($msg ne ''){ 
				$msg .= ', un giorno valido';
			}
			else{
				$msg .= 'Inserire un giorno valido';
			}
		}
	}
}
else {
	$giorno="01";
	$mese="01";
	$anno="1900"; 
}

if($email ne ''){
	if($email !~ /^[\w\.\-]+@\w+[\w\.\-]*?\.\w{1,4}$/){
		if($msg ne ''){ 
			$msg .= ', un indirizzo e-mail valido';
		}
		else{
			$msg .= 'Inserire un indirizzo e-mail valido';
		}
	}
}
else {
	$email='nome.cognome@gmail.com';
}

if($nome eq '') {
	$nome=" ";
}
if($cognome eq '') {
	$cognome=" ";
}

if($citta eq '') {
	$citta=" ";
}
if($prefisso eq '' && $numero eq '' ) {
	$prefisso="123";
	$numero="456789";
}

# controllo sul nome utente
if($username eq ''){
	if($msg ne ''){ 
		$msg .= ', un nome utente';
	}
	else{
		$msg .= 'Inserire un nome utente';
	}
}

$query = "//utente[username='$username']";
$lista = $radice->findnodes($query);
if($lista->size() > 1) {
	if($msg ne ''){ 
		$msg .= ', un nome utente valido (nome utente già scelto)';
	}
	else{
		$msg .= 'Inserire un nome utente valido (nome utente già scelto)';
	}
}

# controlli sulla password
if($password eq ''){
	if($msg ne ''){ 
		$msg .= ', una password';
	}
	else{
		$msg .= 'Inserire una password';
	}
}

if(length $password > 16){
	if($msg ne ''){ 
		$msg .= ', una password valida (max 16 caratteri)';
	}
	else{
		$msg .= 'Inserire una password valida (max 16 caratteri)';
	}
}

if($password ne '' && length $password < 6){
	if($msg ne ''){ 
		$msg .= ', una password valida (min 6 caratteri)';
	}
	else{
		$msg .= 'Inserire una password valida (min 6 caratteri)';
	}
}

if($password ne $confPassword){
	if($msg ne ''){ 
		$msg .= ', confermare la password';
	}
	else{
		$msg .= 'Confermare la password';
	}
}

# se, arrivati a questo punto, sono state rilevate delle irregolarità, viene fatto il redirect alla pagina 
# della form per mostrare il messaggio di errore
if($msg ne ''){
	print $cgi->header(-location=>"registratiForm.cgi?msg=$msg");
	exit;
}

#creo un nuovo utente da inserire nel file xml
my $nuovo_utente="\n\t<utente>
		<nome>".$nome."</nome>
		<cognome>".$cognome."</cognome>
		<amministratore>false</amministratore>
		<username>".$username."</username>
		<datanascita>".$anno."\-".$mese."\-".$giorno."</datanascita>
		<email>".$email."</email>
		<password>".$password."</password>
		<telefono>".$prefisso." ".$numero."</telefono>
		<citta>".$citta."</citta>
	</utente>\n";
				
my $frammento= $parser->parse_balanced_chunk($nuovo_utente) || die(" Nodo non ben formato!");
$radice->appendChild($frammento) || die("Errore nell'inserimento del nuovo nodo");

open(OUT, ">$file_xml");
print OUT $documento->toString;
close(OUT);

print $cgi->header(-location=>"registratiForm.cgi?msg=Registrazione effettuata con successo!");
exit;
