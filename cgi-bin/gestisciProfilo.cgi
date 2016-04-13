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



	my $filedati="../data/utenti.xml";
	my $parser=XML::LibXML->new();	# crea il parser dell'XML
	my $doc=$parser->parse_file($filedati) || die ("Errore nella parserizzazione del file xml");	# associa il parser all'XML
	my $root=$doc->getDocumentElement || die ("Errore nell'estrazione dell'elemento radice");		# individua la radice dell'XML

	print header(-type=>'text/html',
				 -charset=>'UTF-8',
				 -lang=>'it');
				 
	print start_html(-title=>'Gestione profilo - Time Out',
					-dtd=>[ '-//W3C//DTD XHTML 1.0 Strict//EN',
					'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'],
					-head=>meta({-http_equiv => 'Content-Script-Type',
								-content => 'text/javascript'}),
					-meta=>{
					  'description'=>'pagina privata dedicata alla gestione del profilo dei clienti registrati della pizzeria Time Out',
					  'keywords'=>'profilo, utente, time out, pizza, pizzeria, pizzeria per asporto, forno a legna, Torreglia, Abano, Conselve',
					  'language'=>'italian',
					  'author'=>'Berton, Pavanello, Roetta, Rubin'},
					-style => [{'src'=>'../css/style_v2-1.css'},{-verbatim => '@import url("../css/style_v3.css");'}],
					-script => {'src'=>'../js/controlloForm.js'},
					-lang=>'it'); 

print<<EOF;
				<div id="container">
					<div class="mainTitle">
						<img id="logo" width="220"  alt="logo della pizzeria Time Out" src="../images/logosmall.jpg"   />  
						<div class="titles">
								<h1 xml:lang="en">Time Out</h1>
								<h2>Pizzeria per asporto</h2>
						</div>
					
		
						<div class="login-box">
EOF

if ($sid) {
	# se la sessione è valida allora mostro la pagina per la gestione del profilo
	$session = load CGI::Session("driver:File", $sid, {Directory=>'session'});
    $username = $session->param('username'); 

						print "<p>Sei loggato come: <strong>$username</strong></p>
								<p><a href=\"logout.cgi\" tabindex=\"5\">ESCI</a></p>";
} else {
print <<EOF;

							<form method="post" action="login.cgi">
								<div>
									Nome utente: <input title="accesso" type="text" name="user" /><br />
									Password: <input title="accesso" type="password" name="pwd" maxlength="16"/><br /> 
									<input type="hidden" name="page" value="gestisciProfilo.cgi" /> 
									<input class="pulsante" type="submit" value="LOGIN" /> 
									<input class="pulsante" type="button" onclick="location.href='registratiForm.cgi';" value="REGISTRATI" />
								</div>
							</form>	
EOF

	my $msg = $cgi->param("msgErrLogin");
	if($msg ne ''){
		print "<div class=\"msgErrorLogin\">
			 $msg
			</div>";
	}
}

print <<EOF;
						</div>
						<div class="clear-float"> </div>
					</div>
EOF


if ($sid) {
   $session = load CGI::Session("driver:File", $sid, {Directory=>'session'});
   $username = $session->param('username'); 
   $amministratore = $session->param('amministratore');  

print<<EOF;				
					<div class="nav">
						<ul>
							<li class="currentLink">Gestione profilo</li>
EOF
	if($amministratore eq 'true'){ 
		print '<li><a href="gestisciUtenti.cgi" tabindex="1">Gestione utenti</a></li>
				<li><a href="listinoAdmin.cgi" tabindex="2">Gestione listino</a></li>
				<li><a href="commentiAdmin.cgi" tabindex="3">Gestione commenti</a></li>';}
print <<EOF;
						</ul>
					</div>
			
					<div class="path">
						<p>Ti trovi in: <span>Gestione profilo</span></p>
					</div>
EOF

	# definisco la query per recuperare l'utente con lo username dato
	my $query = "//utente[username='$username']";
	my $utente = $doc->findnodes($query)->get_node(1);

	# ricavo i valori dei sottoelementi
	my $nome = $utente->findnodes('nome');
	my $cognome = $utente->findnodes('cognome');
	my $data = $utente->findnodes('datanascita');
	my $citta = $utente->findnodes('citta');
	my $email = $utente->findnodes('email');
	my $telefono = $utente->findnodes('telefono');
	my $password = $utente->findnodes('password');

	# converto la data prima di mostrarla
	@dataScomposta = split(/-/,$data);
	$data = @dataScomposta[2].'/'.@dataScomposta[1].'/'.@dataScomposta[0];

	my $msg = $cgi->param("msg");
	print "	<div class=\"basic-content\">";
	if($msg){
		print "<div class=\"msgError\">$msg</div>";
	}
	print "<h1>Informazioni principali</h1>";
	
	print "			
					<span id=\"checkMsg\" class=\"msgError\"> </span>
					<form action=\"cambiaVoceProfilo.cgi\" method=\"post\">
						<div>
							<label for=\"cvp_nome\">Nome:</label>
							<input type=\"text\" id=\"cvp_nome\" name=\"valore\" value=\"$nome\" />
							<input type=\"hidden\" name=\"voce\" value=\"nome\"/>
							<input type=\"hidden\" name=\"username\"  value=\"$username\"/>
							<input type=\"submit\" value=\"Cambia\"/>
						</div>
					</form>

					<form action=\"cambiaVoceProfilo.cgi\" method=\"post\">
						<div>
							<label for=\"cvp_cognome\">Cognome:</label>
							<input type=\"text\" id=\"cvp_cognome\" name=\"valore\" value=\"$cognome\" />
							<input type=\"hidden\" name=\"voce\" value=\"cognome\"/>
							<input type=\"hidden\" name=\"username\"  value=\"$username\"/>
							<input type=\"submit\" value=\"Cambia\"/>
						</div>
					</form>

					<form action=\"cambiaVoceProfilo.cgi\" method=\"post\">
						<div>
							<label for=\"cvp_datanascita\">Data di nascita:</label>
							<input type=\"text\" id=\"cvp_datanascita\" name=\"valore\" value=\"$data\" />
							<input type=\"hidden\" name=\"voce\" value=\"datanascita\"/>
							<input type=\"hidden\" name=\"username\"  value=\"$username\"/>
							<input type=\"submit\" value=\"Cambia\"/>
						</div>
					</form>

					<form action=\"cambiaVoceProfilo.cgi\" method=\"post\">
						<div>
							<label for=\"cvp_citta\">Citt&agrave;:</label>
							<input type=\"text\" id=\"cvp_citta\" name=\"valore\" value=\"$citta\" />
							<input type=\"hidden\" name=\"voce\" value=\"citta\"/>
							<input type=\"hidden\" name=\"username\"  value=\"$username\"/>
							<input type=\"submit\" value=\"Cambia\"/>
						</div>
					</form>

					<form action=\"cambiaVoceProfilo.cgi\" method=\"post\">
						<div>
							<label for=\"cvp_telefono\">Telefono:</label>
							<input type=\"text\" id=\"cvp_telefono\" name=\"valore\" value=\"$telefono\" maxlength=\"11\" />
							<input type=\"hidden\" name=\"voce\" value=\"telefono\"/>
							<input type=\"hidden\" name=\"username\"  value=\"$username\"/>
							<input type=\"submit\" value=\"Cambia\"/>
						</div>
					</form>

					<form action=\"cambiaVoceProfilo.cgi\" method=\"post\" onsubmit=\"return check(['cvp_email'], ['string'], [false]);\">
						<div>
							<label for=\"cvp_email\"><span xml:lang=\"en\">E-mail</span>:</label>
							<input type=\"text\" title=\"e-mail\" id=\"cvp_email\" name=\"valore\" value=\"$email\" />
							<input type=\"hidden\" name=\"voce\" value=\"email\"/>
							<input type=\"hidden\" name=\"username\"  value=\"$username\"/>
							<input type=\"submit\" value=\"Cambia\"/>
						</div>
					</form>
						

					<h1>Cambio dati di accesso</h1>

					<form action=\"cambiaVoceProfilo.cgi\" method=\"post\" onsubmit=\"return check(['pwd','conf'], ['string','conf'], [true,true]);\">
						<div>
							<label for=\"pwd\">Nuova <span xml:lang=\"en\">password</span>: </label> 
							<input type=\"password\" title=\"password\" id=\"pwd\" maxlength=\"16\" name=\"valore\" />
							<label for=\"conf\">Conferma <span xml:lang=\"en\">password</span>: </label>
							<input type=\"password\" title=\"conferma password\" id=\"conf\" maxlength=\"16\" name=\"confermaPassword\" />
							<input type=\"hidden\" name=\"voce\" value=\"password\"/>
							<input type=\"hidden\" name=\"username\"  value=\"$username\"/>
							<input type=\"submit\" value=\"Cambia\"/>
						</div>
					</form>
					<p class=\"aiuto\">Lunghezza minima <span xml:lang=\"en\">password</span> 6 caratteri, lunghezza massima 16 caratteri.</p>

					<h1>Rimozione <span xml:lang=\"en\">account</span></h1>
					<p><strong>Attenzione</strong>: questa operazione non sar&agrave; reversibile</p>
						<form action=\"rimuoviUtente.cgi\" method=\"post\">
							<div>
								<input type=\"hidden\" name=\"pagina\" value=\"gestisciProfilo\"/>
								<input type=\"hidden\" name=\"username\"  value=\"$username\"/>
								<input type=\"submit\" value=\"Cancella profilo\"/>
							</div>
						</form>
					</div>";	
}
else{
	# se la sessione non è valida specifico con un messaggio che la pagina è riservata
	print "				
					<div class=\"nav\">
						<ul>
							<li><a href=\"home.cgi\" xml:lang=\"en\" tabindex=\"1\">Home</a></li>
							<li><a href=\"listino.cgi\" tabindex=\"2\">Listino pizze</a></li>
							<li><a href=\"commenti.cgi\" tabindex=\"3\">I vostri commenti</a></li>
							<li><a href=\"../contatti.html\" tabindex=\"4\">Dove siamo</a></li>
							<li class=\"currentLink\">Area riservata</li>
						</ul>
					</div>
					<div class=\"path\">
						<p>Ti trovi in: <span>Area riservata</span></p>
					</div>
					<div class=\"msg-content\">
						<h1>Area ad accesso limitato</h1>
						<p>Per accedere a quest'area devi essere registrato ed aver effettuato l'<strong>autenticazione</strong>!</p>
						<p><em>Per autenticarti compila il modulo nella parte superiore della pagina</em></p>
					</div>
	";
} 


		
print <<EOF;
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








