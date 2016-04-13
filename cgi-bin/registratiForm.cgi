#!/usr/bin/perl -w

# librerie utilizzate
use XML::LibXML;
use HTML::Entities;
use CGI;
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use utf8;

my $cgi=new CGI;



print header(-type=>'text/html',
			 -charset=>'UTF-8',
			 -lang=>'it',
			 -head  => meta({-http_equiv => 'Content-Script-Type ', -content => 'text/javascript'})
			 
			 );
			 
print start_html(-head => meta({-http_equiv => 'Content-Script-Type',
					-content => 'text/javascript'}),
				-title=>'Registrati - Time Out',
				-dtd=>[ '-//W3C//DTD XHTML 1.0 Strict//EN',
					'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'],
				-meta=>{
				  'description'=>'pagina per la registrazione degli utenti del sito della catena di pizzerie Time Out',
				  'keywords'=>'registrazione, time out, pizza, pizzeria, pizzeria per asporto, forno a legna, Torreglia, Abano, Conselve',
				  'language'=>'italian',
				  'author'=>'Berton, Pavanello, Roetta, Rubin'
				  },
				-style => [{'src'=>'../css/style_v2-1.css'},{-verbatim => '@import url("../css/style_v3.css");'}],
				-script => {'src'=>'../js/controlloForm.js'},
					-lang=>'it'); 


					
					
					

print <<EOF;
	<div id="container">
			<div class="mainTitle">
				<img id="logo" width="220"  alt="logo della pizzeria Time Out" src="../images/logosmall.jpg"   />  
				<h1 xml:lang="en">Time Out</h1>
				<h2>Pizzeria per asporto</h2>
			</div> 
		
			<div class="nav">
				<ul>
					<li><a href="home.cgi" xml:lang="en" tabindex="1">Home</a></li>
					<li><a href="listino.cgi" tabindex="2">Listino pizze</a></li>
					<li><a href="commenti.cgi" tabindex="3">I vostri commenti</a></li>
					<li><a href="../contatti.html" tabindex="4">Dove siamo</a></li>
					<li><a href="gestisciProfilo.cgi" tabindex="5">Area riservata</a></li>
				</ul>
			</div>
	
			<div class="path">
				<p>Ti trovi in: <span>Registrati</span></p>
			</div>
			
			<div class="content-header">		
				<h1>Vuoi lasciarci un tuo commento ma non sei ancora iscritto?</h1>
				<h2> Allora cosa aspetti...Fallo subito!!! </h2>
			</div>
			
			<div id="registrazione">
EOF

my $msg = $cgi->param("msg");
if($msg ne ''){
	print "<div class=\"msgError\">
		 $msg
		</div>";
}


print <<EOF;

<span id="checkMsg" class="msgError"> </span>
<script type="text/javascript">
   var items = ["username", "password", "conf_password","email","giorno","mese","anno"];
   var types = ["string", "string","string","string","int", "int","int"];
   var required = [true,true,true,false,false,false,false];
</script>
				<form method="post" action="registrati.cgi" onsubmit="javascript: return check(items, types, required);">
					<fieldset>
						<legend> <strong>Registrazione nuovo utente</strong> </legend>
					
						<div>
							<label for="nome"> Nome:</label>
							<input type="text" title="nome" name="nome" id="nome"  />
						</div>
						
						<div>
							<label for="cognome"> Cognome: </label>
							<input type="text" title="cognome" name="cognome" id="cognome" />
						</div>
						
						<div>
							<label for="username"> <span xml:lang="en">Username</span>*:</label>
							<input type="text" title="username" name="username" id="username" maxlength="20"/>
						</div>
						
						<div id="data_utente">
							<span> Data di Nascita (gg/mm/aaaa): </span>
						
								<input title="giorno di nascita" type="text" name="giorno" id="giorno" maxlength="2"/>
								<span>/</span>
								<input title="mese di nascita" type="text" name="mese" id="mese" maxlength="2"/>
								<span>/</span>
								<input title="anno di nascita" type="text" name="anno" id="anno" maxlength="4"/>
							
						</div>

						<div>
							<label for="citta"> Citt&agrave;: </label>
							<input title="luogo di nascita" type="text" name="citta" id="citta" />
						
						</div>
						
						<div id="numtel">
							<label for="prefisso"> Prefisso: </label>
							<input title="prefisso" type="text" name="prefisso" id="prefisso" maxlength="3" />
							<label for="telefono"> Telefono: </label>
							<input title="telefono" type="text" name="numero" id="telefono" maxlength="7" />
						</div>

						<div>
							<label for="email"> <span xml:lang="en">E-mail</span>: </label>
							<input title="e-mail" type="text" name="email" id="email"/>
						</div>
						
						<div>
							<label for="password"> <span xml:lang="en">Password</span>*: </label>
							<input title="password" type="password" name="password" id="password" maxlength="16"/>
						</div>
						
						<div>
							<label for="conf_password"> Conferma <span xml:lang="en">Password</span>*: </label>
							<input title="conferma password" type="password" name="conf_password" id="conf_password" maxlength="16"/>
						</div>
																
						<div>
							<input class="pulsante" type="submit" id="submit" name="submit" value="Invia i tuoi dati"/>
							<p class="aiuto">*Campi obbligatori</p>
							<p class="aiuto">Lunghezza minima <span xml:lang="en">password</span> 6 caratteri, lunghezza massima 16 caratteri.</p>							
						</div>
						
					</fieldset>
				</form>
				
				<span id="collage">  </span>
				<div class="clear-float"></div>
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
