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
use CGI::Cookie;
use utf8;
use CGI "meta";

my $cgi = new CGI;

my $sid = $cgi->cookie("CGISESSID") || undef;

if ($sid) {
   $session = load CGI::Session("driver:File", $sid, {Directory=>'session'});
   $utente = $session->param('username'); 
   $amministratore = $session->param('amministratore');
}

my $filedati="../data/commenti.xml";

my $parser=XML::LibXML->new(); # crea il parser dell'XML
my $doc=$parser->parse_file($filedati) || die ("Errore nel parsing del file xml"); # associa il parser all'XML
my $root=$doc->getDocumentElement || die ("Errore nell'estrazione dell'elemento radice"); # individua la radice dell'XML
my $elencoCom = $root->getElementsByTagName('commento') || die "Errore nella creazione dell'array degli elementi 'commenti'";		# crea un array in cui mette tutti i commenti

# Pagina XHTML 
print $cgi->header(-charset=>'UTF-8',
			-lang => 'it',
			-type=>'text/html');

 print $cgi->start_html( 
		-head => meta({-http_equiv => 'Content-Script-Type',
					-content => 'text/javascript'}),
		-title => 'I vostri commenti - Time Out',
		-dtd=>[ '-//W3C//DTD XHTML 1.0 Strict//EN',
					'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'],
		
		-meta => {'keywords' => 'time out, pizza, pizzeria, pizzeria per asporto, forno a legna, Torreglia, Abano, Conselve, i vostri commenti','description' => 'In questa pagina gli utenti registrati possono lasciare i loro commenti riguardo i prodotti e il servizio delle pizzerie Time Out','author' => 'Berton, Pavanello, Roetta, Rubin'},
		-style => [{'src'=>'../css/style_v2-1.css'},{-verbatim => '@import url("../css/style_v3.css");'}],
				-lang=>'it',
);

# NavBar e Logo
print '
	<div id="container">
		<div class="mainTitle">
							<img id="logo" width="220"  alt="logo della pizzeria Time Out" src="../images/logosmall.jpg"   />  
							<div class="titles">
								<h1 xml:lang="en">Time Out</h1>
								<h2>Pizzeria per asporto</h2>
							</div>
							<div class="login-box">';
if ($sid) {
print "<p>Sei loggato come: <strong>$utente</strong></p>
<p><a href=\"logout.cgi\" tabindex=\"5\">ESCI</a></p>";
} else {
print <<EOF;

		<form method="post" action="login.cgi">
			<div>
				<label for="username">Nome utente: </label>
				<input type="text" id="username" name="user" /></div>
<div><label for="password">Password: </label><input type="password" name="pwd" id="password" maxlength="16" /></div>
		<div>
			<input type="hidden" name="page" value="commenti.cgi" /> 
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
							<div class="clear-float"></div>
				</div> 
		
		<div class="nav">
			<ul>
				<li><a href="../cgi-bin/home.cgi" xml:lang="en" tabindex="1">Home</a></li>
				<li><a href="listino.cgi" tabindex="2">Listino pizze</a></li>
				<li class="currentLink">I vostri commenti</li>
				<li><a href="../contatti.html" tabindex="3">Dove siamo</a></li>
				<li><a href="gestisciProfilo.cgi" tabindex="4">Area riservata</a></li>
			</ul>
		</div>
	
		<div class="path">
			<p>Ti trovi in: <span>I vostri commenti</span></p>
		</div>

EOF
		
# Contenuto della pagina
# Elenco Commenti precedenti
my $totCom = $elencoCom->size();

print '<div class="basic-content">';
for(my $nCom=1; $nCom<=$totCom; $nCom++){
	#prendo un commento e ne leggo gli elementi
	my $commento = $elencoCom->get_node($nCom);	
	
	my $id = $commento->getElementsByTagName("ID");
	my $utente = $commento->getElementsByTagName("utente");
	my $testo = $commento->getElementsByTagName("testo");
	my $sede = $commento->getElementsByTagName("sede");
	my $datadb = $commento->getElementsByTagName("data");
	
	# metto la data in un formato più leggibile
	@dataOra = split(/T/,$datadb);
	@partiData = split(/-/,@dataOra[0]);
	$data = @partiData[2].'/'.@partiData[1].'/'.@partiData[0];
	$ora = @dataOra[1];
	
	if($sid && $session->param('username') eq "$utente"){
		print "<div class=\"quote-box\">
					<div class=\"quote\">
						<form action=\"cambiaCommento.cgi\" method=\"post\">
							<div>
								<textarea title=\"modificaCmmento\" name=\"testo\" rows=\"3\" cols=\"60\">$testo</textarea>
								<input type=\"hidden\" name=\"id\" value=\"$id\" />
								<input type=\"submit\" name=\"submit\" value=\"Modifica\"/>
							</div>
						</form>	
						<form action=\"rimuoviCommento.cgi\" method=\"post\">
							<div>
								<input type=\"hidden\" name=\"id\" value=\"$id\" />
								<input type=\"submit\" name=\"submit\" value=\"Elimina\"/>
							</div>
						</form>	
					</div>
					<p class=\"quote-details\">Commento di <strong>$utente</strong> - Data: <strong>$data $ora</strong> - Sede: <strong>$sede</strong></p>
				</div>";
	}
	else{
		print "<div class=\"quote-box\"><p class=\"quote\">$testo</p>
			<p class=\"quote-details\">Commento di <strong>$utente</strong> - Data: <strong>$data $ora</strong> - Sede: <strong>$sede</strong></p></div>";
	}
}

# Mostra o nascondi finestra inserisci commento
if($sid) {
	print '	<div id="commenta">
				<form method="post" action="aggiungiCommento.cgi" >
					<fieldset>
						<p>Benvenuto '.$utente.'! Per lasciare un commento, compila il form sottostante.</p>
						<legend>Inserisci un nuovo commento</legend>
							
						<input type="hidden" value="'.$utente.'" name="utente" />
						<input type="hidden" value="commenti.cgi" name="pagina" />
												
						<div>
							<label for="testo"> Messaggio: </label>
							<textarea name="testo" id="testo" cols="50" rows="3"></textarea>
							<br />
							<br />

							<label for="sede"> Sede:</label>
							<select title="Sede" id="sede" name="sede">
  								<option value="Torreglia">Torreglia</option>
  								<option value="Conselve">Conselve</option>
    							<option value="Abano Terme">Abano Terme</option>
  							</select>
						</div>
																				
						<div>
							<input type="hidden" name="adddate" id="data" />
							<input type="submit" name="submit" value="Inserisci commento"/>
						</div>
						
					</fieldset>
				</form>
			</div>';	
}

print '</div>';

# Footer della pagina
print '
		<div class="footer" >
			<img id="imgHtmlValidCode" alt="logo validatore w3c per html1.0" src="../images/valid-xhtml10.png"/> 
			<img id="imgCssValidCode" alt="logo validatore w3c per css" src="../images/vcss-blue.gif" />
			<p>Pizzeria <span xml:lang="en">Time Out</span> - Conselve: Tel. 049 950 0629 Via Padova, 19</p>
			<p>Pizzeria <span xml:lang="en">Time Out</span> - Torreglia: Tel. 049 993 0310 Via Montegrotto, 5</p>
			<p>Pizzeria <span xml:lang="en">Time Out</span> - Abano Terme: Tel. 049 860 0418 Via Mazzini, 12</p>
		</div>
	</div>';

print '<script type="text/javascript" src="../js/functions.js"></script>';

print $cgi->end_html;
