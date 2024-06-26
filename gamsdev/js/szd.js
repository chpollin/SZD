///////////////////////////////////////////////
// in entry-footer: copies stefanzweig.digital/o:szd.bibliothek#SZDBIB.285 into clipboard
function copy(id) {
  ta = document.createElement('textarea');
  ta.value = id.textContent;
  document.body.appendChild(ta);
  ta.select();
  document.execCommand('copy');
  document.body.removeChild(ta);
  //alert("Copied: " + "\n" + id.textContent);
}


///////////////////////////////////////////////
$('a[data-toggle="collapse"]').click(function(){
    $(this).find("span.arrow").text(function(i,old){
    return old=='▼ ' ?  '▲ ' : '▼ ';
    });
}); 
                    

///////////////////////////////////////////////
function jump_to_id_switching_language(HREF_URL)
{
 // href="{concat('/', $PID, '/sdef:TEI/get?locale=de')}" 
 console.log(HREF_URL);
 if(location.hash)
 {
    window.location.href = HREF_URL + window.location.hash
 }
 else
 {
     window.location.href = HREF_URL
 }
}

///////////////////////////////////////////////
window.onload = function () {
	const hash = window.location.hash.substr(1);
    if(location.hash){
		location.hash = "#" + hash;
		window.scrollBy(0, -250);
		//select first element with .collapse to open entry and not entry-footer
		$(document.getElementById(hash).getElementsByClassName("collapse")).first().collapse() ;
		}
}


///////////////////////////////////////////////
function scrolldown (src) {
    if (src !== '') {
        if (typeof src !== typeof '') {
            //src = $(src).attr('href');
            location.hash = src;
        }
        //src ist onclick(this) also #CH1 etc.;
        window.setTimeout(function () {
            window.location.href = src;
            //mit der 2. zahl kann man definieren wie weit nach unten (oder nach oben, positive zahl) man gehen möchte
            window.scrollBy(0, -250);
            if($(document.getElementById(src.substr(1)).getElementsByClassName("collapse"))  &&  src.includes('SZD'))
            {
               $(document.getElementById(src.substr(1)).getElementsByClassName("collapse")).first().collapse() ;
            }
        },
        100);
    };

};

///////////////////////////////////////////////
// loading, spinner
function setVisible(selector, visible) {
  document.querySelector(selector).style.display = visible ? 'block' : 'none';
}