#!/usr/bin/perl -w

# librerie utilizzate
use XML::LibXML;
use HTML::Entities;
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);

my $cgi=new CGI;

# crea l'intestazione della pagina html..
print header(-type=>'text/html',
			 -charset=>'UTF-8',
			 -lang=>'it');
print start_html(-title=>'Home - Time Out',
				-dtd=>[ '-//W3C//DTD XHTML 1.0 Strict//EN',
					'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'],
				-meta=>{'home page della catena di pizzerie Time Out',
				  'keywords'=>'home, time out, pizza, pizzeria, pizzeria per asporto, forno a legna, Torreglia, Abano, Conselve',
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
						<li class="currentLink"><span xml:lang="en">Home</span></li>
						<li><a href="listino.cgi" tabindex="1">Listino pizze</a></li>
						<li><a href="commenti.cgi" tabindex="2">I vostri commenti</a></li>
						<li><a href="../contatti.html" tabindex="3">Dove siamo</a></li>
						<li><a href="gestisciProfilo.cgi" tabindex="4">Area riservata</a></li>
					</ul>
				</div>
			
				<div class="path">
					<p>Ti trovi in: <span xml:lang="en">Home</span></p>
				</div>
				
				<div id="left-content">
					<ul id="categories">
						<li id="classiche" ><a href="listino.cgi#classiche" tabindex="5">Le classiche</a></li>
						<li id="calzoni" class="right"><a href="listino.cgi#calzoni" tabindex="6">I calzoni</a></li>
						<li id="baguette" ><a href="listino.cgi#baguette" tabindex="7">Le <span xml:lang="fr">baguette</span></a></li>
						<li id="crostini" class="right"><a href="listino.cgi#crostini" tabindex="8">I crostini</a></li>
						<li id="bianche"><a href="listino.cgi#bianche" tabindex="9">Le bianche</a></li>
						<li id="speciali" class="right"><a href="listino.cgi#speciali" tabindex="10">Le speciali</a></li>
						<li id="bufaline"><a href="listino.cgi#bufaline" tabindex="11">Le bufaline</a></li>
						<li id="fritture"><a href="listino.cgi#fritti" tabindex="12">I fritti</a></li>
					</ul>
					
					<div id="about-us">
						<h1>Pizza per passione...</h1>
						<p> Presso le pizzerie della catena <span xml:lang="en">Time Out</span> a Conselve, Torreglia e Abano Terme puoi gustare pizze 
							squisite, preparate in <strong>forni a legna</strong> come vuole la tradizione e con una vasta gamma di ingredienti di qualità.
						</p>
						<p> Da sempre attenti alle esigenze e ai gusti dei nostri clienti, proponiamo anche pizze impastate con <strong>farina al <span xml:lang="en">Kamut</span></strong>; 
							dal lunedì al venerdì puoi trovare soffici <strong>tranci di pizza</strong> farcita e, da pochi mesi, al lunedì c'è la fantastica <strong>pizza 
							alla romana</strong>!!!
						</p>
					</div>
					
					<div id="party">
					<h2>Vuoi organizzare feste, compleanni o un'abbuffata con gli amici?</h2>
						<p>Conta pure su di noi! Prenota le tue <strong>teglie 
								di tranci</strong> di pizza o prendi le <strong>pizze formato famiglia</strong> da farcire a piacere!!!   
							</p>
					</div>
				</div>

EOF

# leggo dal file news.txt le ultime novità e le stampo nell'apposito riquadro
my $filename = "../data/news.txt";
open(FILE, "<", "$filename") || die "errore nella lettura del file";
my @news = <FILE>;

print "<div id=\"news\" class=\"box\">
			<h2>Ultime <span xml:lang=\"en\">news</span></h2>";
print "@news";
print "</div>";

close FILE;
	
print <<EOF;
			<div id="times" class="box">
				<p><strong>Aperto</strong> dalle <strong>18:00</strong> alle <strong>22:30</strong>  <strong>TUTTI I GIORNI</strong></p> 
			</div>
		
			<!--<div id="img-home" class="box"></div>-->
		
			<img title="Siamo stati premiati!" alt="Il premio al nostro pizzaiolo" class="box" src="../images/premio.jpg" />
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
