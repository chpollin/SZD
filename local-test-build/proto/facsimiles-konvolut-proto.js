// PROTOTYPE (local harness only, not deployed): a third gallery view that groups
// the correspondence facsimiles by the curated konvolut, i.e. the person-based
// edition objects o:szd.korrespondenzen.<person>, instead of the B-signature.
//
// Data: proto/konvolut-map.json, extracted from the TEI index
// o:szd.korrespondenzen (idno[@type='konvolut'] + correspAction persons) and the
// DC titles of the konvolut objects. In production this join would come from the
// gallery QUERY (konvolut PID per piece); here we approximate it by matching the
// server-rendered person heading (slug, then name) to a konvolut.
//
// Hooks into the existing switcher: adds a third button and wraps
// window.setFacsimilesView so the two production modes keep working untouched.
(function () {
	'use strict';

	var MAP_URL = 'http://localhost:8080/local-test-build/proto/konvolut-map.json';
	// cards load IMG.1 (the full master, ~1 MB each); the IIIF image server on
	// gams.uni-graz.at delivers a 400px derivative at ~40 KB (Level 2, CORS open)
	var IIIF_WIDTH = 400;
	var IIIF_BASE = 'https://gams.uni-graz.at/iiif/';
	// bundles with more cards than this start collapsed, with a show-all button
	var COLLAPSE_AFTER = 8;

	function getLocale() {
		var m = window.location.search.match(/[?&]locale=([^&]+)/);
		if (m) { return decodeURIComponent(m[1]).substring(0, 2).toLowerCase(); }
		var l = document.documentElement.getAttribute('lang');
		return (l ? l : 'de').substring(0, 2).toLowerCase();
	}

	function naturalCompare(a, b) {
		return String(a).localeCompare(String(b), undefined, { numeric: true, sensitivity: 'base' });
	}

	// slug normalisation close to what the konvolut PIDs use, so that
	// "Ferencak, Mirko M." and o:szd.korrespondenzen.ferencak-mirko-m can meet
	function slugify(name) {
		return name.toLowerCase()
			.normalize('NFD').replace(/[̀-ͯ]/g, '')
			.replace(/ß/g, 'ss')
			.replace(/[^a-z0-9]+/g, '-')
			.replace(/^-+|-+$/g, '');
	}

	function cleanTitle(t) {
		if (!t || t === 'Untitled') { return null; }
		return t.replace(/:\s*Stefan Zweig digitale?\s*$/, '').trim();
	}

	function init(map) {
		var gallery = document.getElementById('facsimiles-gallery');
		var switcher = document.querySelector('.facsimiles-modeswitch');
		var prodShow = window.setFacsimilesView;
		if (!gallery || !switcher || typeof prodShow !== 'function') { return; }

		var loc = getLocale();
		var L = loc === 'en' ? {
			btn: 'By bundle (edition)', unmapped: 'Without curated bundle', pieces: 'pieces in the index',
			facs: 'with facsimile', sig: 'Signature', partner: 'Partners', link: 'To the bundle view',
			multi: 'physically split over several signatures', collective: '* signature shared with other bundles',
			guessed: 'stack link on the live site points to', showAll: 'Show all', more: 'more'
		} : {
			btn: 'Nach Konvolut (Erschließung)', unmapped: 'Ohne kuratiertes Konvolut', pieces: 'Stücke laut Index',
			facs: 'mit Faksimile', sig: 'Signatur', partner: 'Partner', link: 'Zur Konvolutansicht',
			multi: 'physisch auf mehrere Signaturen verteilt', collective: '* Signatur mit anderen Konvoluten geteilt',
			guessed: 'Stack-Link der Live-Site zeigt auf', showAll: 'Alle anzeigen', more: 'weitere'
		};

		// index lookups: slug -> konvolut, partner name -> konvolut, signature -> [konvolute]
		var bySlug = {}, byName = {}, bySig = {};
		Object.keys(map).forEach(function (pid) {
			var k = map[pid];
			bySlug[pid.replace('o:szd.korrespondenzen.', '')] = k;
			k.partners.forEach(function (n) { byName[n] = byName[n] || k; });
			k.signatures.forEach(function (s) { (bySig[s] = bySig[s] || []).push(pid); });
		});

		// rewrite /o:szd.NNN/IMG.1 to the IIIF derivative, in whatever view is shown
		function useThumbnails(root) {
			Array.prototype.forEach.call(root.querySelectorAll('img.card-img-top'), function (img) {
				var m = (img.getAttribute('src') || '').match(/^\/?(o:szd\.[^/]+)\/(IMG\.\d+)$/);
				if (m) { img.src = IIIF_BASE + m[1] + '/' + m[2] + '/full/' + IIIF_WIDTH + ',/0/default.jpg'; }
			});
		}

		// hide cards beyond COLLAPSE_AFTER and add a button that reveals them
		function collapseLarge(root) {
			Array.prototype.forEach.call(root.querySelectorAll('.gallery-block .row'), function (row) {
				if (row.getAttribute('data-collapsed')) { return; }
				var cards = row.children;
				if (cards.length <= COLLAPSE_AFTER) { return; }
				for (var i = COLLAPSE_AFTER; i < cards.length; i++) { cards[i].hidden = true; }
				var wrap = document.createElement('div');
				wrap.className = 'col-12 text-center my-2';
				var btn = document.createElement('button');
				btn.type = 'button';
				btn.className = 'btn btn-outline-secondary btn-sm facsimiles-showall';
				btn.textContent = L.showAll + ' (' + (cards.length - COLLAPSE_AFTER) + ' ' + L.more + ')';
				btn.addEventListener('click', function () {
					Array.prototype.forEach.call(row.children, function (c) { c.hidden = false; });
					wrap.remove();
				});
				wrap.appendChild(btn);
				row.appendChild(wrap);
				row.setAttribute('data-collapsed', 'true');
			});
		}

		useThumbnails(gallery);
		collapseLarge(gallery);

		var personHTML = gallery.innerHTML;
		var cachedHTML = null;

		function resolve(slug, name) {
			return bySlug[slug] || byName[name] || bySlug[slugify(name)] || null;
		}

		function headingText(b) {
			if (!b.konvolut) { return b.personName; }
			return cleanTitle(b.konvolut.title) || ('Korrespondenz ' + b.personName);
		}

		function heading(b) {
			var wrap = document.createElement('div');
			var h2 = document.createElement('h2');
			h2.className = b.konvolut ? 'mt-5 facsimiles-konvolut-heading' : 'mt-4 h4 facsimiles-konvolut-heading';
			h2.id = 'konvolut-' + b.slug;
			h2.textContent = headingText(b) + ' ';
			if (b.konvolut) {
				var a = document.createElement('a');
				a.href = 'https://stefanzweig.digital/' + b.konvolut.pid;
				a.target = '_blank';
				a.className = 'ml-1 small';
				a.title = L.link;
				a.textContent = b.konvolut.pid;
				h2.appendChild(a);
			}
			wrap.appendChild(h2);

			var p = document.createElement('p');
			p.className = 'text-muted small';
			var parts = [];
			if (b.konvolut) {
				var k = b.konvolut;
				parts.push(k.extent + ' ' + L.pieces + ', ' + b.cards.length + ' ' + L.facs);
				if (k.signatures.length) {
					var shared = false;
					var sigs = k.signatures.map(function (s) {
						var isShared = (bySig[s] || []).length > 1;
						shared = shared || isShared;
						return s + (isShared ? ' *' : '');
					});
					parts.push(L.sig + ' ' + sigs.join(', '));
					if (k.signatures.length > 1) { parts.push(L.multi); }
					if (shared) { parts.push(L.collective); }
				}
				if (k.partners.length > 1) { parts.push(L.partner + ' ' + k.partners.join('; ')); }
			} else {
				parts.push(b.cards.length + ' ' + L.facs);
				parts.push(L.guessed + ' o:szd.korrespondenzen.' + b.slug);
			}
			p.textContent = parts.join(' | ');
			wrap.appendChild(p);
			return wrap;
		}

		function build() {
			var tmp = document.createElement('div');
			tmp.innerHTML = personHTML;

			// walk the server-rendered person sections: h2 followed by its gallery block
			var buckets = {}, order = [];
			Array.prototype.forEach.call(tmp.querySelectorAll('h2[id]'), function (h2) {
				var slug = h2.id;
				var name = h2.textContent.trim();
				var block = h2.nextElementSibling;
				var k = resolve(slug, name);
				var key = k ? k.pid : 'unmapped:' + slug;
				if (!buckets[key]) {
					buckets[key] = { konvolut: k, personName: name, slug: slug, cards: [], seen: {} };
					order.push(key);
				}
				var b = buckets[key];
				if (!block) { return; }
				Array.prototype.forEach.call(block.querySelectorAll('[data-pid]'), function (card) {
					var pid = card.getAttribute('data-pid');
					if (b.seen[pid]) { return; }
					b.seen[pid] = true;
					var clone = card.cloneNode(true);
					clone.hidden = false;
					b.cards.push(clone);
				});
			});

			// curated konvolute first, unmapped persons at the end
			order.sort(function (a, b) {
				var ua = a.indexOf('unmapped:') === 0, ub = b.indexOf('unmapped:') === 0;
				if (ua !== ub) { return ua ? 1 : -1; }
				// sort by the person heading (surname first); the DC titles mix
				// "Forename Surname" and "Surname, Forename" and would scatter the order
				return naturalCompare(buckets[a].personName, buckets[b].personName);
			});

			var holder = document.createElement('div');
			var unmappedIntro = false;
			order.forEach(function (key) {
				var b = buckets[key];
				if (!b.konvolut && !unmappedIntro) {
					unmappedIntro = true;
					var sep = document.createElement('h2');
					sep.className = 'mt-5 text-muted';
					sep.textContent = L.unmapped;
					holder.appendChild(sep);
				}
				holder.appendChild(heading(b));
				var block = document.createElement('div');
				block.className = 'gallery-block cards-gallery';
				var row = document.createElement('div');
				row.className = 'row';
				b.cards.sort(function (x, y) {
					return naturalCompare(x.getAttribute('data-signatur') || '', y.getAttribute('data-signatur') || '');
				}).forEach(function (c) { row.appendChild(c); });
				block.appendChild(row);
				holder.appendChild(block);
			});
			return holder.innerHTML;
		}

		// third button next to the two production ones
		var btn = document.createElement('button');
		btn.type = 'button';
		btn.className = 'view-tab';
		btn.setAttribute('data-mode', 'erschliessung');
		btn.id = 'facsimiles-view-erschliessung';
		btn.setAttribute('role', 'tab');
		btn.setAttribute('aria-controls', 'facsimiles-gallery');
		btn.setAttribute('aria-selected', 'false');
		btn.tabIndex = -1;
		btn.textContent = L.btn;
		btn.addEventListener('click', function () { window.setFacsimilesView('erschliessung'); });
		switcher.appendChild(btn);

		window.setFacsimilesView = function (mode) {
			if (mode !== 'erschliessung') {
				prodShow(mode);
				useThumbnails(gallery);
				collapseLarge(gallery);
				return;
			}
			if (cachedHTML === null) { cachedHTML = build(); }
			gallery.innerHTML = cachedHTML;
			collapseLarge(gallery);
			gallery.setAttribute('data-view', 'erschliessung');
			var nav = document.querySelector('.header-card-nav ul.list-inline');
			if (nav) { nav.style.display = 'none'; }
			Array.prototype.forEach.call(switcher.querySelectorAll('[data-mode]'), function (x) {
				var selected = x.getAttribute('data-mode') === mode;
				x.classList.toggle('active', selected);
				x.setAttribute('aria-selected', String(selected));
				x.tabIndex = selected ? 0 : -1;
			});
			gallery.setAttribute('aria-labelledby', btn.id);
		};
	}

	function start() {
		fetch(MAP_URL).then(function (r) { return r.json(); }).then(init).catch(function (e) {
			console.error('konvolut-proto: map not loaded', e);
		});
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', start);
	} else {
		start();
	}
})();
