

/*Funktion fuer scrolldown oder auch scrollup (zb. von Fussnoten) unter die sticky Navigationsleiste
Die Anchor Tags die zum Sprungpunk verlinken müssen ein onlclick="scrolldown(this)" Attribut bekommen! */

function scrolldown (src) {
    if (src !== '') {
        if (typeof src !== typeof '') {
            src = $(src).attr('href');
        }
        //src ist onclick(this) also #CH1 etc.;
        window.setTimeout(function () {
            window.location.href = src;
            //mit der 2. zahl kann man definieren wie weit nach unten (oder nach oben, positive zahl) man gehen möchte
            window.scrollBy(0, -0);
        },
        100);
    };

};

