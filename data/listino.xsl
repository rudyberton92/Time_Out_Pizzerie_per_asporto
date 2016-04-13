<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method='html' version='1.0' encoding='UTF-8' indent='yes'
	doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
	doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" />

	<xsl:template match="/" >

		<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="it" lang="it">
			
			<head>
				<meta http-equiv="Content-Type" content="text/html; charset=utf8"/>
				<title>	Listino - Time Out	</title>
				<link rel="stylesheet" href="../css/style_v2-1.css" type="text/css"/> 
				

				<meta name="description" content="listino della catena di pizzerie Time Out"/>
				<meta name="keywords" content="listino, time out, pizza, pizzeria, pizzeria per asporto, forno a legna, Torreglia, Abano, Conselve, classiche, calzoni, baguette, bianche, mozz. di bufala, crostini, fritture"/>
				<meta name="language" content="italian"/>
				<meta name="author" content="Berton, Pavanello, Roetta, Rubin" />
				
				<style type="text/css">
					@import url("css/style_v3.css");
				</style>			
			</head>

			<body>
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
							<li><a href="home.cgi" xml:lang="en">Home</a></li>
							<li class="currentLink">Listino pizze</li>
							<li><a href="commenti.cgi">I vostri commenti</a></li>
							<li><a href="contatti.html">Dove siamo</a></li>
							<li><a href="gestisciProfilo.cgi">Area riservata</a></li>
						</ul>
					</div>
				
					<div class="path">
						<p>Ti trovi in: Listino</p>
					</div>

					<div id="listino">
						<xsl:for-each select="listino/categoria">
							<h1> 
								
								<xsl:attribute name="id">
										<xsl:value-of select="@id" />
								</xsl:attribute>
								<xsl:value-of select="@nome"/>
								
							</h1>
						
							<xsl:choose>
							
								<xsl:when test="@nome = 'I Fritti'">
									<ul>
									
										<xsl:for-each select="fritto">
											<li xml:space="preserve"> 
												<span class="nome"><xsl:value-of select="@nome"/></span> - <xsl:value-of select="prezzo"/> <xsl:value-of select="prezzo/@valuta"/>  
												<br/><em><xsl:value-of select="descrizione"/></em>
											</li>
										</xsl:for-each>
										
									</ul>
								</xsl:when>
								
								<xsl:otherwise>
									<ul>
										
										<xsl:for-each select="pizza">
											<li>
												<span xml:space="preserve"><span class="nome"><xsl:value-of select="@nome"/></span> - <xsl:value-of select="prezzo"/> <xsl:value-of select="prezzo/@valuta"/></span>
												<br/><em>
													<xsl:for-each select="ingredienti/ingrediente">
														<xsl:value-of select="text()"/>, 
													</xsl:for-each>
												</em>
											</li>
										</xsl:for-each>
										
									</ul>
								</xsl:otherwise>
								
							</xsl:choose>
							<a href="../cgi-bin/trasformaListino.cgi">Torna su</a>
					</xsl:for-each>
					</div>
					

					<div class="footer" > 
						<img id="imgHtmlValidCode" alt="logo validatore w3c per html1.0" src="../images/valid-xhtml10.png"/> 
						<img id="imgCssValidCode" alt="logo validatore w3c per css" src="../images/vcss-blue.gif" />
						<p>Pizzeria <span xml:lang="en">Time Out</span> - Conselve: Tel. 049 950 0629 Via Padova, 19</p>
						<p>Pizzeria <span xml:lang="en">Time Out</span> - Torreglia: Tel. 049 993 0310 Via Montegrotto, 5</p>
						<p>Pizzeria <span xml:lang="en">Time Out</span> - Abano Terme: Tel. 049 860 0418 Via Mazzini, 12</p>
					</div>
					
				</div>
			</body>

		</html>

	</xsl:template> 
        
</xsl:stylesheet>
