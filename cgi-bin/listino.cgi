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
print start_html(-title=>'Listino - Time Out',
				-dtd=>[ '-//W3C//DTD XHTML 1.0 Strict//EN',
					'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'],
				-meta=>{
				  'description'=>'listino della catena di pizzerie Time Out',
				  'keywords'=>'listino, time out, pizza, pizzeria, pizzeria per asporto, forno a legna, Torreglia, Abano, Conselve',
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
							<div class="clear-float"></div>
				</div> 

				<div class="nav">
					<ul>
						<li><a href="home.cgi" xml:lang="en" tabindex="1">Home</a></li>
						<li class="currentLink">Listino pizze</li>
						<li><a href="commenti.cgi" tabindex="2">I vostri commenti</a></li>
						<li><a href="../contatti.html" tabindex="3">Dove siamo</a></li>
						<li><a href="gestisciProfilo.cgi" tabindex="4">Area riservata</a></li>
					</ul>
				</div>
			
				<div class="path">
					<p>Ti trovi in: <span>Listino pizze</span></p>
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
	
	if($nomeCategoria ne "I Fritti"){
	  @pizze = $categoria->findnodes("pizza");
	  $nPizzePerCategoria = @pizze;
	  	  
          print '<ul>';
	  foreach $pizza(@pizze){
		  my $nomePizza = $pizza->getAttribute("nome");
		  my $prezzo = ($pizza->findnodes("prezzo"))[0];	# restituisco il primo e unico nodo della lista ritornata da findnodes()
		 
		  print '<li><span class="nome">'.$nomePizza.'</span> - '.$prezzo->textContent.' '.$prezzo->getAttribute("valuta").'';

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
		  print '<br /><em>'.$ingredientiPizza.'</em></li>';
		  
	  }
          print '</ul>';
	 }
	else{
	  #$categoria->findnodes("fritto") restituisce UNA LISTA i cui nodi contengono sono ELEMENTI 'fritto'
	  @fritti = $categoria->findnodes("fritto");
	  $nFritti = @fritti;
	  
	  print '<ul>';  
	  foreach $fritto(@fritti){
		 		  
		  my $prezzo = ($fritto->findnodes("prezzo"))[0];	# restituisco il primo e unico nodo della lista ritornata da findnodes()
		  my $nomeFritto = $fritto->getAttribute("nome");
		  my $descrizioneScalar = ($fritto->findnodes("descrizione"))[0];
		  my $descrizione = $descrizioneScalar->to_literal;
		  		  	
		  print '<li><span class="nome">'.$nomeFritto.'</span> - '.$prezzo->to_literal.' '.$prezzo->getAttribute("valuta").'<br /><em>'.$descrizione.'</em></li>';
	  }
          print '</ul>';
	}
	print '<a class="linkHelp" href="listino.cgi" tabindex="5">Torna su</a>';
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
