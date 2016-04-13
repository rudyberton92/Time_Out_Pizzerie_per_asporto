#!/usr/bin/perl -w

# librerie utilizzate
use XML::LibXML;
use HTML::Entities;
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use CGI::Session();
use CGI::Cookie;
use utf8;

my $cgi=new CGI;

my $sid = $cgi->cookie("CGISESSID") || undef;

if ($sid) {
   $session = load CGI::Session("driver:File", $sid, {Directory=>'session'});
   $sutente = $session->param('username'); 
   $amministratore = $session->param('amministratore');
   
   if($amministratore eq 'true'){

		my $filedati="../data/utenti.xml";
		my $parser=XML::LibXML->new();	# crea il parser dell'XML
		my $doc=$parser->parse_file($filedati) || die ("Errore nella parserizzazione del file xml");	# associa il parser all'XML
		my $root=$doc->getDocumentElement || die ("Errore nell'estrazione dell'elemento radice");		# individua la radice dell'XML
		my $utenti = $root->getElementsByTagName('utente') || die "Errore nella creazione dell'array degli elementi 'utente'";

		print header(-type=>'text/html',
					 -charset=>'UTF-8',
					 -lang=>'it');
		print start_html(-title=>'Gestione utenti - Time Out',
						-dtd=>[ '-//W3C//DTD XHTML 1.0 Strict//EN',
					'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'],
						-meta=>{
						  'description'=>'pagina privata dedicata all\'anagrafica e alla gestione degli accessi dei clienti registrati della pizzeria Time Out',
						  'keywords'=>'profilo, utente, accessi, amministratore, time out, pizza, pizzeria, pizzeria per asporto, forno a legna, Torreglia, Abano, Conselve',
						  'language'=>'italian',
						  'author'=>'Berton, Pavanello, Roetta, Rubin'},
		-style => [{'src'=>'../css/style_v2-1.css'},{-verbatim => '@import url("../css/style_v3.css");'}],
						-lang=>'it'); 

print <<EOF;
			<div id="container">
				<div class="mainTitle">
					<img id="logo" width="220"  alt="logo della pizzeria Time Out" src="../images/logosmall.jpg"   />  
					<div class="titles">
								<h1 xml:lang="en">Time Out</h1>
								<h2>Pizzeria per asporto</h2>
						</div>
					
		
						<div class="login-box">
							<p>Sei loggato come: <strong>$sutente</strong></p>
							<p><a href=\"logout.cgi\" tabindex="4">ESCI</a></p>
						</div>
	
						<div class="clear-float"> </div>
					</div>  
				
				<div class="nav">
					<ul>
						<li><a href="gestisciProfilo.cgi" tabindex="1">Gestione profilo</a></li>
						<li class="currentLink">Gestione utenti</li>
						<li><a href="listinoAdmin.cgi" tabindex="2">Gestione listino</a></li>
						<li><a href="commentiAdmin.cgi" tabindex="3">Gestione commenti</a></li>
					</ul>
				</div>
			
				<div class="path">
					<p>Ti trovi in: <span>Gestione utenti</span></p>
				</div>
				<div class="basic-content">
EOF


		my $totUtenti = $utenti->size();
		print "<p class=\"users-amount\">Numero utenti: <strong>$totUtenti</strong></p>";

		for(my $nUt=1; $nUt<=$totUtenti; $nUt++){
			# per ogni utente ricavo le informazioni del profilo
			my $utente = $utenti->get_node($nUt);

			my $nome = ($utente->findnodes('nome'))[0]->textContent;
			my $cognome = ($utente->findnodes('cognome'))[0]->textContent;
			my $username = ($utente->findnodes('username'))[0]->textContent;
			my $dataNascita = ($utente->findnodes('datanascita'))[0]->textContent;
			my $citta = ($utente->findnodes('citta'))[0]->textContent;
			my $mail = ($utente->findnodes('email'))[0]->textContent;
			my $telefono = ($utente->findnodes('telefono'))[0]->textContent;
			my $accesso = ($utente->findnodes('amministratore'))[0]->textContent;

			if($nome eq ' ' && $cognome eq ' ') {
				$nome="Nome";
				$cognome="Cognome";
				}

			# converto la data prima di mostrarla
			@dataScomposta = split(/-/,$dataNascita);
			$dataNascita = @dataScomposta[2].'/'.@dataScomposta[1].'/'.@dataScomposta[0];

			# stampo tutte le informazioni dell'utente, compreso il livello attuale di accesso,
			# e prevedo i comandi per cambiare i privilegi di accesso
			print "
					
						<div class=\"user-box\">
							<h1 title=\"Nome e cognome\">$nome $cognome</h1>
							<p>Username: $username </p>
							<p>Data di nascita: $dataNascita </p>
							<p>Citt&agrave;: $citta </p>
							<p><span xml:lang=\"en\">E-mail</span>: $mail</p>
							<p>Telefono: $telefono </p>
							<p>Accesso: $accesso</p>";
							
			if($sutente ne $username){
							print "<form action=\"cambiaPermessi.cgi\" method=\"post\">
								<div>";
			
				if($accesso eq 'true'){
							print "	<fieldset class=\"noFieldset\">
									<legend class=\"noLegend\">Ruolo</legend>
									<input title=\"Amministratore\" type=\"radio\" name=\"accesso\" value=\"true\" checked=\"checked\" />Amministratore
									<input title=\"Cliente\" type=\"radio\" name=\"accesso\" value=\"false\"/>Cliente
									</fieldset>";
							
				}
				else{
							print "	<fieldset class=\"noFieldset\">
									<legend class=\"noLegend\">Ruolo</legend>
									<input title=\"Amministratore\" type=\"radio\" name=\"accesso\" value=\"true\"/>Amministratore
									<input title=\"Cliente\" type=\"radio\" name=\"accesso\" value=\"false\" checked=\"checked\" />Cliente
									</fieldset>";
				}
			
						print "	
								<input type=\"hidden\" name=\"username\" value=\"$username\"/>
								<input type=\"submit\" value=\"Cambia privilegi\"/>
								</div>
							</form>
							<form action=\"rimuoviUtente.cgi\" method=\"post\">
								<div>
									<input type=\"hidden\" name=\"username\" value=\"$username\"/>
									<input type=\"submit\" value=\"Rimuovi utente\"/>
								</div>
							</form>";
			}
			print "</div>";
		}

print <<EOF;
			</div>
			<div class="footer" > 
					<img id="imgHtmlValidCode" alt="logo validatore w3c per html1.0" src="../images/valid-xhtml10.png"/> 
					<img id="imgCssValidCode" alt="logo validatore w3c per css" src="../images/vcss-blue.gif" />
					<p>Pizzeria <span xml:lang="en">Time Out</span> - Conselve: Tel. 049 950 0629 Via Padova, 19</p>
					<p>Pizzeria <span xml:lang="en">Time Out</span> - Torreglia: Tel. 049 993 0310 Via Montegrotto, 5</p>
					<p>Pizzeria <span xml:lang="en">Time Out</span> - Abano Terme: Tel. 049 860 0418 Via Mazzini, 12</p>
			</div>	
		</div>
	
EOF
print end_html;
	}
}
