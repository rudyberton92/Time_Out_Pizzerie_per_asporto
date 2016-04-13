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

if ("$sid") {
   $session = load CGI::Session("driver:File", $sid, {Directory=>'session'});
   $utente = $session->param('username'); 
   $amministratore = $session->param('amministratore');
}

my $filedati="../data/listino.xml";
my $parser=XML::LibXML->new();	# crea il parser dell'XML
my $doc=$parser->parse_file($filedati) || die ("Errore nella parserizzazione del file xml");	# associa il parser all'XML
my $root=$doc->getDocumentElement || die ("Errore nell'estrazione dell'elemento radice");		# individua la radice dell'XML
my $categorie = $root->getElementsByTagName('categoria') || die "Errore nella creazione dell'array degli elementi 'categoria'";		# crea un array in cui mette tutti i commenti
# crea l'intestazione della pagina html..

# $root->getElementsByTagName('categoria') ritorna UNA lista di nodi in cui OGNI nodo contiene UNA categoria

print header(-type=>'text/html',
			 -charset=>'UTF-8',
			 -lang=>'it');
print start_html(-title=>'Gestione listino - Time Out',
				-dtd=>[ '-//W3C//DTD XHTML 1.0 Strict//EN',
					'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'],
				-meta=>{
				  'description'=>'In questa pagina privata gli amministratori del sito possono aggiornare il listino dei prodotti',
				  'keywords'=>'listino, time out, pizza, pizzeria, pizzeria per asporto, forno a legna, Torreglia, Abano, Conselve',
				  'language'=>'italian',
				  'author'=>'Berton, Pavanello, Roetta, Rubin'},
				-style => [{'src'=>'../css/style_v2-1.css'},{-verbatim => '@import url("../css/style_v3.css");'}],
				-head=>meta({-http_equiv => 'Content-Script-Type',
								-content => 'text/javascript'}),
				-script => {'src'=>'../js/controlloForm.js'},
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
EOF

if ($sid) {
						print "<p>Sei loggato come: <strong>$utente</strong></p>
								<p><a href=\"logout.cgi\" tabindex=\"4\">ESCI</a></p>";
} else {
print <<EOF;

							<form method="POST" action="login.cgi">
								Nome utente: <input type="text" name="user" value="rberton" /><br />Password: <input type="password" name="pwd" value="123456" /><br /> <input type="hidden" name="page" value="listino.cgi" /> <input type="submit" value="LOGIN" /> <input type="button" onclick="location.href='../registrati.html';" value="REGISTRATI" />
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
						<li class="currentLink">Gestione listino</li>
						<li><a href="commentiAdmin.cgi" tabindex="3">Gestione commenti</a></li>
					</ul>
				</div>
			
				<div class="path">
					<p>Ti trovi in: <span>Gestione listino</span></p>
				</div>
				
				<div class="basic-content">
EOF


print <<EOF;
				  <form action="aggiungiVoceListino.cgi" method="post">
					  <fieldset id=\"formProdotto\"> <legend>Form di inserimento di un nuovo prodotto</legend>
						  <div>
							  <label for="categoria">Categoria: </label>
							  <select name="categoria" id="categoria">
								  <option value="Classiche">Classiche</option>
								  <option value="Speciali">Speciali</option>
								  <option value="I Crostini">Crostini</option>
								  <option value="Calzoni">Calzoni</option>
								  <option value="Baguette">Baguette</option>
								  <option value="Bufaline">Bufaline</option>
								  <option value="I Fritti">Fritti</option>
							  </select>
						  </div>
						  <div>
							  <label for="nome">Nome prodotto: </label>	<input name="nome" id="nome"/>
							  <label for="prezzo">Prezzo:</label> <input name="prezzo" onchange="checkDecimal(document.getElementById('prezzo'));" id="prezzo"/>
						  </div>
						  <div>
							  <label for="ingredienti">Ingredienti: </label> <input type="text" name="ingredienti" id="ingredienti"/>
						  </div>
						  <div>
							  <label for="descrizione">Descrizione (solo per i fritti): </label> <input type="text" name="descrizione" id="descrizione"/>
						  </div>
						  <div>
							  <input type="submit" value="Inserisci"/>
						  </div>
					  </fieldset>
				  </form>
				</div>
				
				<div id="listino">

EOF

my $nCategorie = $categorie->size();

# in questo primo ciclo l'indice parte da 1 perchè uso il metodo get_node() per scorrere i nodi xml
for($c=1; $c<=$nCategorie; $c++){	
	
	$categoria = $categorie->get_node($c);	#categoria ha tipo Nodo
	
	$nomeCategoria = $categoria->getAttribute("nome");
	$idCategoria = $categoria->getAttribute("id");
	
	print '<h1 id="'.$idCategoria.'">'.$nomeCategoria.'</h1>';
	
	if($nomeCategoria ne "I Fritti"){ # voglio gestire la stampa di un elemento pizza
	  @pizze = $categoria->findnodes("pizza");
	  $nPizzePerCategoria = @pizze;
	  	  
	  print '<ul>';
	  foreach $pizza(@pizze){
		  my $nomePizza = $pizza->getAttribute("nome");
		  my $prezzo = ($pizza->findnodes("prezzo"))[0];	# restituisco il primo e unico nodo della lista ritornata da findnodes()
		 
		  print '<li><span class="nome">'.$nomePizza.'</span>';

		  my $ingredientiPizza = "";
		  my $temp = ($pizza->findnodes("ingredienti"))[0];	# temp contiene il nodo 'ingredienti'
		  my @ingredienti = $temp->findnodes("ingrediente");	# ingredienti è una  lista di nodi 'ingrediente'
		  my $nIngredienti = @ingredienti;

		  
		  my $primoIngrediente = 1;
		  foreach $ingrediente(@ingredienti){
			  $ingrediente = $ingrediente->textContent;
			  
			  
			  if($primoIngrediente == 1) { 
				  $ingredientiPizza .= $ingrediente; 
				  $primoIngrediente = 0;
			  }
			  else { $ingredientiPizza .= ', '.$ingrediente; }
		  }
		  print '<br /><em>'.$ingredientiPizza.'</em>';
		  

		  print "<form class=\"inline\" action=\"cambiaPrezzo.cgi\" method=\"post\">
		  			<div>
						Prezzo: <input type=\"text\" onchange=\"checkDecimal(this);\" value=\"".$prezzo->textContent."\" name=\"prezzoDaCambiare\" title=\"prezzoDaCambiare\" /> ".$prezzo->getAttribute("valuta")."&nbsp;&nbsp;
						<input type=\"hidden\" name=\"categoria\" value=\"$nomeCategoria\"/>
						<input type=\"hidden\" name=\"nome\"  value=\"$nomePizza\"/> 
						<input type=\"submit\" value=\"Cambia\"/>
					</div>
				</form>";
		  print "<form class=\"inline\" action=\"rimuoviProdotto.cgi\" method=\"post\">
		  			<div>
						<input type=\"hidden\" name=\"nome\"  value=\"$nomePizza\"/>
						<input class=\"spazio\" type=\"submit\" value=\"Elimina\"/>
					</div>
				</form></li>";
		  
	  }
          print '</ul>';
	 }
	else{ # voglio getire la stampa di un elemento pizza
	  #$categoria->findnodes("fritto") restituisce UNA LISTA i cui nodi contengono sono ELEMENTI 'fritto'
	  @fritti = $categoria->findnodes("fritto");
	  $nFritti = @fritti;
	  
	  print '<ul>';	  
	  foreach $fritto(@fritti){
		 		  
		  my $prezzo = ($fritto->findnodes("prezzo"))[0];	# restituisco il primo e unico nodo della lista ritornata da findnodes()
		  my $nomeFritto = $fritto->getAttribute("nome");
		  my $descrizioneScalar = ($fritto->findnodes("descrizione"))[0];
		  my $descrizione = $descrizioneScalar->to_literal;
		 
		  		  
		  print '<li><span class="nome">'.$nomeFritto.'</span><br /><em>'.$descrizione.'</em>';
		  print "<form  class=\"inline\" action=\"cambiaPrezzo.cgi\" method=\"post\">
		  			<div>
						Prezzo:<input type=\"text\" onchange=\"checkDecimal(this);\" value=\"".$prezzo->to_literal."\" name=\"prezzoDaCambiare\" title=\"prezzoDaCambiare\" /> ".$prezzo->getAttribute("valuta")."&nbsp;&nbsp;
						<input type=\"hidden\" name=\"categoria\" value=\"$nomeCategoria\"/>
						<input type=\"hidden\" name=\"nome\" value=\"$nomeFritto\"/>
						<input type=\"hidden\" name=\"descrizione\" value=\"$descrizione\"/>
						<input type=\"submit\" value=\"Cambia prezzo\"/>
					</div>
				</form>";
		  print "<form class=\"inline\" action=\"rimuoviProdotto.cgi\" method=\"post\">
		  			<div>
						<input type=\"hidden\" name=\"nome\" value=\"$nomeFritto\"/>
						<input type=\"hidden\" name=\"descrizione\" value=\"$descrizione\"/>
						<input class=\"spazio\" type=\"submit\" value=\"Elimina\"/>
					</div>
				</form> </li>";

	  }
          print '</ul>';
	}
}

print '</div>';

	
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
