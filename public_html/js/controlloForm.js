function check(items, types, required){
	var checkMsg = "";
	var index;

	for (index = 0; index < items.length; ++index) {
	    var iValue = document.getElementById(items[index]).value;
	    var iTitle = document.getElementById(items[index]).title;

		if(required[index] == true) {
			// controllo sui campi obbligatori
			if(iTitle != "conferma password" && iValue == "") {
				if(checkMsg == "") checkMsg = "Inserire " + iTitle;
	    			else checkMsg += ", inserire " + iTitle;
			} else if (iValue == "") {
				if(checkMsg == "") checkMsg = "Confermare password";
				else checkMsg += ", confermare password";
			}
		}
		
		if(iTitle == "password"){
			// controllo sulla lunghezza della password
			if(iValue.length < 6 || iValue.length > 16) {
				if(checkMsg == "") checkMsg = "Lunghezza password non valida";
				else checkMsg += ", lunghezza password non valida";
			}
		}
		if(iTitle == "conferma password" && iValue.length != document.getElementById("password").value.length) {
			// controllo su conferma password
			if(checkMsg == "") checkMsg = "Verificare password";
			else checkMsg += ", verificare password";
		}

		if(iValue != "") {
			// controllo sui campi NON obbligatori
			if(iTitle == "giorno di nascita"){
				if(parseInt(iValue)<1 || parseInt(iValue)>31 || iValue.length<2) {
					if(checkMsg == "") checkMsg = "Inserire un giorno di nascita valido";
					else checkMsg += ", inserire un giorno di nascita valido";
				}
			}
			if(iTitle == "mese di nascita"){
				if(parseInt(iValue)<1 || parseInt(iValue)>12 || iValue.length<2){
					if(checkMsg == "") checkMsg = "Inserire un mese di nascita valido";
					else checkMsg += ", inserire un mese di nascita valido";
				}
			}
			if(iTitle == "anno di nascita"){
				if(iValue.length<4){
					if(checkMsg == "") checkMsg = "Inserire un anno di nascita valido";
					else checkMsg += ", inserire un anno di nascita valido";
				}
			}
			if(iTitle == "e-mail"){
				var pattern = /([a-zA-Z0-9_.-])+@([a-zA-Z0-9_-])+.([a-zA-Z])+([a-zA-Z])+/;
				if(pattern.test(iValue) == false) {
					if(checkMsg == "") checkMsg = "Inserire un indirizzo e-mail valido";
					else checkMsg += ", inserire un indirizzo e-mail valido";
				}
			}
		}
	}
      
	if(checkMsg != ""){
		var elemento = document.getElementById('checkMsg');
		elemento.innerHTML = checkMsg;
		elemento.className = "msgError show"; 
		return false;
	} else return true;
}

function checkDecimal(number) {
	number.value = number.value.replace(",", ".");

	if(number.value.indexOf(".") == -1)
	number.value+='.00';
}

