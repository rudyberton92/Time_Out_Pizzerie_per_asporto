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


my $cgi = new CGI;

# Sono autenticato?
my $sid = $cgi->cookie("CGISESSID") || undef;

if ($sid) {
	$session = load CGI::Session("driver:File", $sid, {Directory=>'session'});
	$utente = $session->param('username'); 
	$amministratore = $session->param('amministratore');
	if ($amministratore eq 'false') {
		print $cgi->header(-location=>"commenti.cgi");
	}
}

my $filedati="../data/commenti.xml";

my $parser=XML::LibXML->new(); # crea il parser dell'XML
my $doc=$parser->parse_file($filedati) || die ("Errore nel parsing del file xml"); # associa il parser all'XML
my $root=$doc->getDocumentElement || die ("Errore nell'estrazione dell'elemento radice"); # individua la radice dell'XML
my $elencoCom = $root->getElementsByTagName('commento') || die "Errore nella creazione dell'array degli elementi 'commenti'";		# crea un array in cui mette tutti i commenti

# Pagina XHTML
print $cgi->header(-charset=>'UTF-8'), 
	$cgi->start_html( 
		-title => 'Gestione commenti - Time Out',
		-dtd=>[ '-//W3C//DTD XHTML 1.0 Strict//EN',
					'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'],
		-lang => 'it',
		-meta => {
			'keywords' => 'time out, pizza, pizzeria, pizzeria per asporto, forno a legna, Torreglia, Abano, Conselve, i vostri commenti',
			'description' => 'In questa pagina privata gli amministratori del sito possono visualizzare, ed eventualmente cancellare, tutti i commenti lasciati in bacheca dai clienti',
			'author' => 'Berton, Pavanello, Roetta, Rubin'},
		-style => [{'src'=>'../css/style_v2-1.css'},{-verbatim => '@import url("../css/style_v3.css");'}],
				-lang=>'it' 
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
<p><a href=\"logout.cgi\" tabindex=\"4\">ESCI</a></p>";
} else {
print <<EOF;

							<form method="POST" action="login.cgi">
								Nome utente: <input type="text" name="user" value="rberton" /><br />
								Password: <input type="password" name="pwd" value="123456" /><br />
								<input type="hidden" name="page" value="commenti.cgi" /> 
								<input type="submit" value="LOGIN" /> 
								<input type="button" onclick="location.href='../registrati.html';" value="REGISTRATI" />
							</form>	
EOF
}

print <<EOF;

							</div>
							<div class="clear-float"></div>
				</div> 
		
		<div class="nav">
			<ul>
				<li><a href="gestisciProfilo.cgi" tabindex="1">Gestione profilo</a></li>
				<li><a href="gestisciUtenti.cgi" tabindex="2">Gestione utenti</a></li>
				<li><a href="listinoAdmin.cgi" tabindex="3">Gestione listino</a></li>
				<li class="currentLink">Gestione commenti</li>
			</ul>
		</div>
			
		<div class="path">
			<p>Ti trovi in: <span>Gestione commenti</span></p>
		</div>

EOF
		
# Contenuto della pagina
# Elenco Commenti precedenti
my $totCom = $elencoCom->size();

print '<div class="basic-content">';
for(my $nCom=1; $nCom<=$totCom; $nCom++){
	#prendo un commento e ne leggo gli elementi
	my $com = $elencoCom->get_node($nCom);	
	
	my $id = $com->getElementsByTagName("ID");
	my $utente = $com->getElementsByTagName("utente");
	my $testo = $com->getElementsByTagName("testo");
	my $sede = $com->getElementsByTagName("sede");
	my $data = $com->getElementsByTagName("data");
	
	# metto la data in un formato più leggibile
	@dataOra = split(/T/,$data);
	@partiData = split(/-/,@dataOra[0]);
	$data = @partiData[2].'/'.@partiData[1].'/'.@partiData[0];
	$ora = @dataOra[1];

	if($sid && $session->param('username') eq "$utente"){
		print "<div class=\"quote-box\">
					<div class=\"quote\">
						<form action=\"cambiaCommento.cgi\" method=\"post\">
							<div>
								<textarea title=\"Inserire il testo\" name=\"testo\" rows=\"3\" cols=\"60\">$testo</textarea>
								<input type=\"hidden\" name=\"id\" value=\"$id\"/>
								<input type=\"hidden\" name=\"page\" value=\"commentiAdmin\" />
								<input type=\"submit\" name=\"submit\" value=\"Modifica\"/>
							</div>
						</form>
						<form action=\"rimuoviCommento.cgi\" method=\"post\">
							<div>
								<input type=\"hidden\" name=\"id\" value=\"$id\"/>
								<input type=\"hidden\" name=\"page\" value=\"commentiAdmin\" />
								<input type=\"submit\" name=\"elimina\" value=\"Elimina\"/>
							</div>
						</form>	
					</div>
					<p class=\"quote-details\">Commento di <strong>$utente</strong> - Data: <strong>$data $ora</strong> - Sede: <strong>$sede</strong></p>
				</div>";
	}
	else{
		print "<div class=\"quote-box\"><div class=\"quote\">
						<form action=\"rimuoviCommento.cgi\" method=\"post\">
							<div>
								<textarea title=\"testo da eliminare\" readonly=\"readonly\" rows=\"3\" cols=\"60\">$testo</textarea>
								<input type=\"hidden\" name=\"id\" value=\"$id\"/>
								<input type=\"hidden\" name=\"page\" value=\"commentiAdmin\" />
								<input type=\"submit\" name=\"submit\" value=\"Elimina\"/>
							</div>
						</form>	
					</div>
			<p class=\"quote-details\">Commento di <strong>$utente</strong> - Data: <strong>$data $ora</strong> - Sede: <strong>$sede</strong></p></div>";
	}
}

# Mostra o nascondi finestra inserisci commento
if($sid) { 
	print "	<div id=\"commenta\">
				<form method=\"post\" action=\"aggiungiCommento.cgi\" >
					<fieldset>
						<p>Benvenuto $utente! Per lasciare un commento, compila il form sottostante.</p>
						<legend>Inserisci un nuovo commento</legend>
							
						<input type=\"hidden\" value=\"$utente\" name=\"utente\" />
						<input type=\"hidden\" value=\"commentiAdmin.cgi\" name=\"pagina\" />
												
						<div>
							<label for=\"testo\"> Messaggio: </label>
							
								<textarea name=\"testo\" id=\"testo\"  cols=\"50\" rows=\"5\"></textarea>
							<br />
							<br />

							<label for=\"sede\"> Sede:</label>
							<select title=\"Scelta della sede\" id=\"sede\" name=\"sede\">
  								<option value=\"Torreglia\">Torreglia</option>
  								<option value=\"Conselve\">Conselve</option>
    							<option value=\"Abano Terme\">Abano Terme</option>
  							</select>
						</div>
																				
						<div>
							<input type=\"hidden\" name=\"adddate\" id=\"data\" />
							<input type=\"submit\" name=\"submit\" value=\"Inserisci commento\"/>
						</div>
						
					</fieldset>
				</form>
			</div>";	
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
