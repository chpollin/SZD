$(function() {
    var suche = "#fulltext_search" ;
    $(suche).on('submit', function () {
        form2params($(suche)) ;
        return false;
    });
});

function form2params(form) {
     var params = "";
     var patt = new RegExp(/^\$[0-9]{1,6}$/);
     $('#fulltext_search :input').each(function() {
        if (patt.test(this.name) && ((this.value != '' && this.type!='radio' && this.type!='checkbox')|| this.checked)) { //select?
            if (params != '') {
                params += ";"
            }
            var value = encodeURIComponent(this.value) ; //Das hier kann durch eine komplexere Funktion ersetzt werden, in der z.B. andere Formularfelder zusammegefügt werden.
            //$1|Goethe;$2|en
            params += this.name + "|" + value + ';$2|' + this.lang;
	}
    });
	var actionUrl = form.attr('action') + "params=" + encodeURIComponent(params) ;
     
    window.location.href=actionUrl.trim();
    return false ;
}
