function setLocalData() {
	data = new Date();
	secondi = data.getSeconds();
	minuti = data.getMinutes();
	ore = data.getHours();
	giorno = data.getDate();
	mese = data.getMonth()+1;
	anno = data.getFullYear();

	if (mese < 10) { mese = '0' + mese; }
	if (giorno < 10) { giorno = '0' + giorno; }
	if (ore < 10) { ore = '0' + ore; }
	if (minuti < 10) { minuti = '0' + minuti; }
	if (secondi < 10) { secondi = '0' + secondi; }

	document.getElementById('data').value = anno+'-'+mese+'-'+giorno+'T'+ore+':'+minuti+':'+secondi;
}

document.onload=setLocalData();
