/*Funktion fuer scrolldown oder auch scrollup (zb. von Fussnoten) unter die sticky Navigationsleiste
Die Anchor Tags die zum Sprungpunk verlinken mĆ¼ssen ein onlclick="scrolldown(this)" Attribut bekommen! */

function scrolldown (src) {
    if (src !== '') {
        if (typeof src !== typeof '') {
            src = $(src).attr('href');
        }
        //src ist onclick(this) also #CH1 etc.;
        window.setTimeout(function () {
            window.location.href = src;
            window.scrollBy(0, -260);
        },
        100);
    };

//window.onload = scrolldown(window.location.hash);
};

