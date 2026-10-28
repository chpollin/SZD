/* Zeitleiste mit Lanes (prototype for o:szd.lebenskalender?mode=timeline).
   Reads the derived lane files of the data repository and shows biography,
   correspondence, personal documents and autographs as switchable lanes on one
   year scale. Written so that the file can move to js/ unchanged: an IIFE, one
   global function, no dependency on jQuery or Bootstrap. */
(function () {
	'use strict';

	var LANES = ['biography', 'correspondence', 'personal-documents', 'autographs'];
	var ICONS = {
		'biography': 'fa-user',
		'correspondence': 'fa-envelope',
		'personal-documents': 'fa-file-alt',
		'autographs': 'fa-feather'
	};
	var SITE = 'https://stefanzweig.digital/';
	// the person search of the live site, same shape the Lebenskalender page uses
	var PERSON_SEARCH = SITE + 'archive/objects/query:szd.person_search/methods/sdef:Query/get'
		+ '?params=%241%7C%3Chttps%3A%2F%2Fgams.uni-graz.at%2Fo%3Aszd.personen%23{ID}%3E%3B%242%7C{LOC}&locale={LOC}';
	// Zweig died in 1942, the estate correspondence runs a few years on. Anything later
	// is a misread date in the source; such pieces leave the view and are reported.
	var MAX_YEAR = 1950;
	// rough block size of one entry, used for the placeholder of an unrendered year
	var ROW_HEIGHT = { biography: 76, other: 54, compact: 26 };

	var T = {
		de: {
			title: 'Zeitleiste',
			lanes: { 'biography': 'Leben', 'correspondence': 'Briefe', 'personal-documents': 'Lebensdokumente', 'autographs': 'Autographen' },
			full: 'Volltext', compact: 'Kompakt', filters: 'Filter',
			place: 'Ort', allPlaces: 'Alle Orte', placeSearch: 'Ort suchen',
			person: 'Person', personHint: 'Name eingeben',
			undated: 'Ohne Datum', yearOnly: 'nur Jahr', range: 'Zeitraum', inferred: 'erschlossen',
			acquired: 'Erwerb', created: 'Entstehung', facsimile: 'Faksimile', detail: 'Detailseite',
			remove: 'Filter entfernen', scale: 'Jahresskala',
			empty: 'Keine Einträge für diese Auswahl.',
			entries: function (n) { return n === 1 ? '1 Eintrag' : n + ' Einträge'; }
		},
		en: {
			title: 'Timeline',
			lanes: { 'biography': 'Life', 'correspondence': 'Letters', 'personal-documents': 'Personal documents', 'autographs': 'Autographs' },
			full: 'Full text', compact: 'Compact', filters: 'Filters',
			place: 'Place', allPlaces: 'All places', placeSearch: 'search a place',
			person: 'Person', personHint: 'type a name',
			undated: 'Undated', yearOnly: 'year only', range: 'date range', inferred: 'inferred',
			acquired: 'acquired', created: 'created', facsimile: 'Facsimile', detail: 'Detail page',
			remove: 'remove filter', scale: 'Year scale',
			empty: 'No entries for this selection.',
			entries: function (n) { return n === 1 ? '1 entry' : n + ' entries'; }
		}
	};

	var state = { lang: 'de', density: 'full', place: null, person: '', from: null, to: null, lanes: {} };
	var events = [];
	var yearMin = 0, yearMax = 0, yearCount = 0;
	var el = {};
	var observer = null;
	var cursorObserver = null;

	function t() { return T[state.lang]; }

	function icon(name, extra) {
		var i = document.createElement('i');
		i.className = 'fas ' + name + (extra ? ' ' + extra : '');
		i.setAttribute('aria-hidden', 'true');
		return i;
	}

	function precisionRank(e) {
		var p = e.datePrecision;
		if (p === 'range' || p === 'inferred') { return 0; }
		if (p === 'year') { return 1; }
		return 2;
	}

	function prepare(byLane) {
		var list = [];
		var beyond = [];
		LANES.forEach(function (lane) {
			(byLane[lane] || []).forEach(function (e) {
				e.year = e.date ? e.date.substring(0, 4) : '';
				e.personIndex = (e.persons || []).map(function (p) { return (p.name || '').toLowerCase(); }).join(' | ');
				if (e.year && +e.year > MAX_YEAR) { beyond.push(e); return; }
				list.push(e);
			});
		});
		if (beyond.length) {
			// a data finding, not a display problem: report it where the caller sees it
			console.warn('Zeitleiste: ' + beyond.length + ' events dated after ' + MAX_YEAR
				+ ' are withheld from scale and list, the dates are misread in the source: '
				+ beyond.map(function (e) { return e.id + ' ' + e.date; }).join(', '));
		}
		// within a year: periods and inferred dates first, then the year-only pieces,
		// then month and day precision in date order; undated pieces last of all
		list.sort(function (a, b) {
			if (a.year !== b.year) { return a.year === '' ? 1 : b.year === '' ? -1 : (a.year < b.year ? -1 : 1); }
			var ra = precisionRank(a), rb = precisionRank(b);
			if (ra !== rb) { return ra - rb; }
			var da = a.date || '', db = b.date || '';
			if (da !== db) { return da < db ? -1 : 1; }
			if (a.lane !== b.lane) { return LANES.indexOf(a.lane) - LANES.indexOf(b.lane); }
			return a.id < b.id ? -1 : a.id > b.id ? 1 : 0;
		});
		return list;
	}

	function personHit(e) {
		return e.personIndex.indexOf(state.person.toLowerCase()) >= 0;
	}

	function matches(e, ignore) {
		if (ignore !== 'lane' && !state.lanes[e.lane]) { return false; }
		if (ignore !== 'place' && state.place && e.place !== state.place) { return false; }
		if (state.person && !personHit(e)) { return false; }
		if (state.from !== null) {
			if (!e.year) { return false; }
			var y = +e.year;
			if (y < state.from || y > state.to) { return false; }
		}
		return true;
	}

	/* ---------- state in the URL ---------- */

	function readUrl() {
		var q = new URLSearchParams(document.location.search);
		// the URL is the whole state, so everything absent falls back to its default
		state.lang = 'de';
		state.density = 'full';
		state.from = null;
		state.to = null;
		LANES.forEach(function (lane) { state.lanes[lane] = true; });
		if (q.get('lanes')) {
			var on = q.get('lanes').split(',');
			LANES.forEach(function (lane) { state.lanes[lane] = on.indexOf(lane) >= 0; });
		}
		if (q.get('lang') === 'en' || q.get('lang') === 'de') { state.lang = q.get('lang'); }
		if (q.get('density') === 'compact') { state.density = 'compact'; }
		state.place = q.get('place') || null;
		state.person = q.get('person') || '';
		var from = parseInt(q.get('from'), 10), to = parseInt(q.get('to'), 10);
		if (from && to) { state.from = Math.min(from, to); state.to = Math.max(from, to); }
	}

	function writeUrl() {
		if (!window.history || !window.history.replaceState) { return; }
		var q = new URLSearchParams();
		var off = LANES.filter(function (lane) { return !state.lanes[lane]; });
		if (off.length) { q.set('lanes', LANES.filter(function (lane) { return state.lanes[lane]; }).join(',')); }
		if (state.lang !== 'de') { q.set('lang', state.lang); }
		if (state.density !== 'full') { q.set('density', state.density); }
		if (state.place) { q.set('place', state.place); }
		if (state.person) { q.set('person', state.person); }
		if (state.from !== null) { q.set('from', state.from); q.set('to', state.to); }
		// built from the document URL, because history resolves a relative URL against
		// the base element, which points at the live site
		var url = new URL(document.location.href);
		url.search = q.toString();
		window.history.replaceState(null, '', url.href);
	}

	/* ---------- controls ---------- */

	function chip(label, count, pressed, onClick, cls) {
		var b = document.createElement('button');
		b.type = 'button';
		b.className = 'zl-chip' + (cls ? ' ' + cls : '');
		b.setAttribute('aria-pressed', String(pressed));
		var text = document.createElement('span');
		text.textContent = label;
		b.appendChild(text);
		if (count !== null) {
			var c = document.createElement('span');
			c.className = 'zl-count';
			c.textContent = count;
			b.appendChild(c);
		}
		b.addEventListener('click', onClick);
		return b;
	}

	function buildLaneChips() {
		el.lanes.innerHTML = '';
		LANES.forEach(function (lane) {
			var n = events.filter(function (e) { return e.lane === lane && matches(e, 'lane'); }).length;
			var b = chip(t().lanes[lane], n, !!state.lanes[lane], function () {
				state.lanes[lane] = !state.lanes[lane];
				render();
			}, 'zl-lane-chip zl-lane-' + lane);
			b.insertBefore(icon(ICONS[lane], 'zl-icon'), b.firstChild);
			el.lanes.appendChild(b);
		});
	}

	function placeCounts() {
		var counts = {};
		events.forEach(function (e) {
			if (!e.place || !matches(e, 'place')) { return; }
			counts[e.place] = (counts[e.place] || 0) + 1;
		});
		return counts;
	}

	function buildPlaceSelect() {
		var counts = placeCounts();
		var names = Object.keys(counts).sort(function (a, b) { return counts[b] - counts[a] || a.localeCompare(b); });
		if (state.place && names.indexOf(state.place) < 0) { names.unshift(state.place); }
		el.placeButton.textContent = state.place ? t().place + ' ' + state.place : t().place;
		el.placeButton.appendChild(icon('fa-caret-down'));
		el.placeSearch.setAttribute('aria-label', t().placeSearch);
		el.placeSearch.placeholder = t().placeSearch;
		var needle = el.placeSearch.value.trim().toLowerCase();
		el.placeList.innerHTML = '';
		el.placeList.appendChild(placeOption(t().allPlaces, null, null));
		names.forEach(function (name) {
			if (needle && name.toLowerCase().indexOf(needle) < 0) { return; }
			el.placeList.appendChild(placeOption(name, counts[name] || 0, name));
		});
	}

	function placeOption(label, count, value) {
		var li = document.createElement('li');
		var b = document.createElement('button');
		b.type = 'button';
		b.setAttribute('aria-current', String(state.place === value));
		var name = document.createElement('span');
		name.textContent = label;
		b.appendChild(name);
		if (count !== null) {
			var c = document.createElement('span');
			c.className = 'zl-count';
			c.textContent = count;
			b.appendChild(c);
		}
		b.addEventListener('click', function () {
			state.place = value;
			closePlaces();
			render();
			el.placeButton.focus();
		});
		li.appendChild(b);
		return li;
	}

	function openPlaces() {
		el.placePopup.hidden = false;
		el.placeButton.setAttribute('aria-expanded', 'true');
		el.placeSearch.focus();
	}

	function closePlaces() {
		el.placePopup.hidden = true;
		el.placeButton.setAttribute('aria-expanded', 'false');
		el.placeSearch.value = '';
	}

	function buildActiveFilters() {
		el.active.innerHTML = '';
		if (state.place) {
			el.active.appendChild(removable(t().place + ' ' + state.place, function () {
				state.place = null;
				render();
			}));
		}
		if (state.person) {
			el.active.appendChild(removable(t().person + ' ' + state.person, function () {
				state.person = '';
				render();
			}));
		}
		if (state.from !== null) {
			el.active.appendChild(removable(state.from + '–' + state.to, function () {
				state.from = null;
				state.to = null;
				render();
			}));
		}
	}

	function removable(label, onClick) {
		var b = chip(label + ' ×', null, true, onClick);
		b.title = t().remove;
		return b;
	}

	function buildPersonList() {
		var names = {};
		events.forEach(function (e) {
			if (!state.lanes[e.lane]) { return; }
			(e.persons || []).forEach(function (p) { if (p.name) { names[p.name] = true; } });
		});
		el.personList.innerHTML = '';
		Object.keys(names).sort().forEach(function (name) {
			var o = document.createElement('option');
			o.value = name;
			el.personList.appendChild(o);
		});
	}

	/* ---------- scale ---------- */

	function laneYearCounts() {
		var counts = {};
		LANES.forEach(function (lane) { counts[lane] = {}; });
		events.forEach(function (e) {
			if (!e.year || !state.lanes[e.lane]) { return; }
			if (state.place && e.place !== state.place) { return; }
			if (state.person && !personHit(e)) { return; }
			counts[e.lane][e.year] = (counts[e.lane][e.year] || 0) + 1;
		});
		return counts;
	}

	function buildScale() {
		var counts = laneYearCounts();
		el.plot.innerHTML = '';
		el.scale.style.setProperty('--zl-cols', yearCount);
		LANES.forEach(function (lane) {
			if (!state.lanes[lane]) { return; }
			var max = 1;
			Object.keys(counts[lane]).forEach(function (y) { max = Math.max(max, counts[lane][y]); });
			var row = document.createElement('div');
			row.className = 'zl-lane-row zl-lane-' + lane;
			row.dataset.lane = lane;
			// the bars repeat what the axis below announces, so they stay out of the
			// accessibility tree and the year links carry the numbers
			row.setAttribute('aria-hidden', 'true');
			for (var y = yearMin; y <= yearMax; y++) {
				var n = counts[lane][String(y)] || 0;
				var cell = document.createElement('span');
				if (n) {
					cell.className = 'zl-bar';
					cell.style.blockSize = Math.max(2, Math.round(12 * n / max)) + 'px';
				}
				row.appendChild(cell);
			}
			el.plot.appendChild(row);
		});
		var cursor = document.createElement('div');
		cursor.className = 'zl-cursor';
		cursor.hidden = true;
		el.plot.appendChild(cursor);
		el.cursor = cursor;
		var brush = document.createElement('div');
		brush.className = 'zl-brush';
		brush.hidden = true;
		el.plot.appendChild(brush);
		el.brush = brush;
		if (state.from !== null) { showBrush(state.from, state.to); }

		el.axis.innerHTML = '';
		for (var yy = yearMin; yy <= yearMax; yy++) {
			el.axis.appendChild(axisCell(yy, counts));
		}
	}

	function axisCell(year, counts) {
		var a = document.createElement('a');
		a.href = '#y' + year;
		a.dataset.year = year;
		var parts = [];
		LANES.forEach(function (lane) {
			if (!state.lanes[lane]) { return; }
			var n = counts[lane][String(year)] || 0;
			if (n) { parts.push(t().lanes[lane] + ' ' + n); }
		});
		a.setAttribute('aria-label', year + (parts.length ? ', ' + parts.join(', ') : ''));
		if (year % 10 === 0) { a.className = 'decade'; }
		if (year % 10 === 0) {
			var lbl = document.createElement('span');
			lbl.className = 'zl-lbl';
			lbl.textContent = year;
			a.appendChild(lbl);
		}
		return a;
	}

	function yearAt(clientX) {
		var box = el.plot.getBoundingClientRect();
		var i = Math.floor((clientX - box.left) / box.width * yearCount);
		return Math.min(yearMax, Math.max(yearMin, yearMin + i));
	}

	function showBrush(from, to) {
		if (!el.brush) { return; }
		var a = Math.min(from, to) - yearMin, b = Math.max(from, to) - yearMin + 1;
		el.brush.hidden = false;
		el.brush.style.insetInlineStart = (a / yearCount * 100) + '%';
		el.brush.style.inlineSize = ((b - a) / yearCount * 100) + '%';
	}

	// year and numbers per lane appear at the pointer or at the focused year, not as a
	// standing line under the scale
	function showTip(year) {
		var counts = laneYearCounts();
		var parts = [String(year)];
		LANES.forEach(function (lane) {
			if (!state.lanes[lane]) { return; }
			parts.push(t().lanes[lane] + ' ' + (counts[lane][String(year)] || 0));
		});
		el.tip.textContent = parts.join(' · ');
		el.tip.hidden = false;
		el.tip.style.insetInlineStart = ((year - yearMin + 0.5) / yearCount * 100) + '%';
	}

	function hideTip() {
		el.tip.hidden = true;
	}

	function jumpTo(year) {
		var head = document.getElementById('y' + year);
		if (!head) { return; }
		var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		head.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
		if (window.history && window.history.replaceState) {
			var url = new URL(document.location.href);
			url.hash = 'y' + year;
			window.history.replaceState(null, '', url.href);
		}
	}

	function bindScale() {
		el.axis.addEventListener('mouseover', function (ev) {
			var a = ev.target.closest('a[data-year]');
			if (a) { showTip(+a.dataset.year); }
		});
		el.axis.addEventListener('focusin', function (ev) {
			var a = ev.target.closest('a[data-year]');
			if (a) { showTip(+a.dataset.year); }
		});
		el.axis.addEventListener('focusout', hideTip);
		el.scale.addEventListener('mouseleave', hideTip);
		el.axis.addEventListener('click', function (ev) {
			var a = ev.target.closest('a[data-year]');
			if (!a) { return; }
			ev.preventDefault();
			jumpTo(a.dataset.year);
		});

		// dragging over the bars selects a period; the year links of the axis keep
		// their jump, so the scale still works where pointer events do not
		var dragFrom = null, dragX = 0;
		el.plot.addEventListener('pointerdown', function (ev) {
			dragFrom = yearAt(ev.clientX);
			dragX = ev.clientX;
			if (el.plot.setPointerCapture) { el.plot.setPointerCapture(ev.pointerId); }
			showBrush(dragFrom, dragFrom);
		});
		el.plot.addEventListener('pointermove', function (ev) {
			var y = yearAt(ev.clientX);
			showTip(y);
			if (dragFrom === null) { return; }
			showBrush(dragFrom, y);
		});
		el.plot.addEventListener('pointerup', function (ev) {
			if (dragFrom === null) { return; }
			var y = yearAt(ev.clientX);
			var moved = Math.abs(ev.clientX - dragX) > 3;
			var from = dragFrom;
			dragFrom = null;
			if (!moved) {
				if (state.from === null) { el.brush.hidden = true; } else { showBrush(state.from, state.to); }
				jumpTo(y);
				return;
			}
			state.from = Math.min(from, y);
			state.to = Math.max(from, y);
			render();
		});
	}

	/* ---------- list ---------- */

	function personLink(p, loc) {
		if (!p.id) {
			var span = document.createElement('span');
			span.textContent = p.name;
			return span;
		}
		var a = document.createElement('a');
		a.href = PERSON_SEARCH.replace('{ID}', p.id).replace(/\{LOC\}/g, loc);
		a.target = '_blank';
		a.rel = 'noopener';
		a.textContent = p.name;
		return a;
	}

	function mark(text) {
		var s = document.createElement('span');
		s.className = 'zl-mark';
		s.textContent = text;
		return s;
	}

	function dateColumn(e, loc) {
		var col = document.createElement('div');
		var where = document.createElement('div');
		where.className = 'zl-where';
		where.appendChild(icon(ICONS[e.lane], 'zl-lane-icon'));
		where.appendChild(document.createTextNode(e.place || ''));
		var when = document.createElement('div');
		when.className = 'zl-when';
		if (e.datePrecision === 'year') { when.appendChild(mark(t().yearOnly)); }
		if (e.datePrecision === 'range') { when.appendChild(mark(t().range)); }
		if (e.datePrecision === 'inferred') { when.appendChild(mark(t().inferred)); }
		var label = (e.dateLabel && (e.dateLabel[loc] || e.dateLabel.de)) || '';
		// the date of an autograph is the date Zweig acquired it, not its origin
		if (e.lane === 'autographs' && label && e.datePrecision !== 'undated') { label = t().acquired + ' ' + label; }
		when.appendChild(document.createTextNode(label));
		col.appendChild(where);
		col.appendChild(when);
		return col;
	}

	function metaLine(e, loc) {
		var meta = document.createElement('div');
		meta.className = 'zl-meta';
		if (e.signature) { meta.appendChild(document.createTextNode(e.signature)); }
		if (e.dateOriginLabel && (e.dateOriginLabel[loc] || e.dateOriginLabel.de)) {
			if (meta.childNodes.length) { meta.appendChild(document.createTextNode(' · ')); }
			meta.appendChild(document.createTextNode(t().created + ' ' + (e.dateOriginLabel[loc] || e.dateOriginLabel.de)));
		}
		if (e.href) {
			if (meta.childNodes.length) { meta.appendChild(document.createTextNode(' · ')); }
			var d = document.createElement('a');
			d.href = e.href;
			d.target = '_blank';
			d.rel = 'noopener';
			d.textContent = t().detail;
			meta.appendChild(d);
		}
		if (e.facsimile) {
			meta.appendChild(document.createTextNode(' '));
			var f = document.createElement('a');
			f.className = 'zl-fac';
			f.href = SITE + e.facsimile;
			f.target = '_blank';
			f.rel = 'noopener';
			f.setAttribute('aria-label', t().facsimile + ' ' + e.facsimile);
			f.title = f.getAttribute('aria-label');
			f.appendChild(icon('fa-image'));
			meta.appendChild(f);
		}
		return meta;
	}

	function row(e) {
		var loc = state.lang;
		var art = document.createElement('article');
		art.className = 'zl-ev zl-lane-' + e.lane;
		art.id = e.id;
		art.dataset.lane = e.lane;
		art.appendChild(dateColumn(e, loc));

		var body = document.createElement('div');
		var text = document.createElement('div');
		text.className = 'zl-text';
		// an autograph is known by its author first, the title of the piece follows
		if (e.lane === 'autographs' && e.persons && e.persons.length) {
			e.persons.forEach(function (p, i) {
				if (i) { text.appendChild(document.createTextNode(', ')); }
				text.appendChild(personLink(p, loc));
			});
			text.appendChild(document.createTextNode('. '));
		}
		text.appendChild(document.createTextNode((e.title && (e.title[loc] || e.title.de)) || ''));
		body.appendChild(text);

		if (e.lane === 'biography' && e.persons && e.persons.length) {
			var pers = document.createElement('div');
			pers.className = 'zl-meta zl-persons';
			e.persons.forEach(function (p, i) {
				if (i) { pers.appendChild(document.createTextNode(', ')); }
				pers.appendChild(personLink(p, loc));
			});
			body.appendChild(pers);
		}

		var meta = metaLine(e, loc);
		if (meta.childNodes.length) { body.appendChild(meta); }
		art.appendChild(body);
		return art;
	}

	function estimate(list) {
		return list.reduce(function (sum, e) {
			if (e.lane === 'biography') { return sum + ROW_HEIGHT.biography; }
			return sum + (state.density === 'compact' ? ROW_HEIGHT.compact : ROW_HEIGHT.other);
		}, 0);
	}

	function heading(id, text, count) {
		var h = document.createElement('h3');
		h.className = 'zl-year';
		h.id = id;
		var title = document.createElement('span');
		title.className = 'zl-year-title';
		title.textContent = text;
		h.appendChild(title);
		var c = document.createElement('span');
		c.className = 'zl-year-count';
		c.textContent = t().entries(count);
		h.appendChild(c);
		return h;
	}

	function group(id, headingText, list) {
		var sec = document.createElement('section');
		sec.className = 'zl-group';
		sec.appendChild(heading(id, headingText, list.length));
		var box = document.createElement('div');
		box.className = 'zl-placeholder';
		box.style.minBlockSize = estimate(list) + 'px';
		sec.appendChild(box);
		sec.rowsToRender = list;
		sec.rowBox = box;
		return sec;
	}

	function fill(sec) {
		if (!sec.rowsToRender) { return; }
		var frag = document.createDocumentFragment();
		sec.rowsToRender.forEach(function (e) { frag.appendChild(row(e)); });
		sec.rowBox.style.minBlockSize = '';
		sec.rowBox.appendChild(frag);
		sec.rowsToRender = null;
	}

	// only the groups in or near the viewport carry their entries, so that more than
	// two thousand of them stay fluid; the cost is a restricted browser search
	function observeGroups(sections) {
		if (observer) { observer.disconnect(); }
		if (!('IntersectionObserver' in window)) {
			sections.forEach(fill);
			return;
		}
		observer = new IntersectionObserver(function (entries) {
			entries.forEach(function (en) {
				if (!en.isIntersecting) { return; }
				fill(en.target);
				observer.unobserve(en.target);
			});
		}, { rootMargin: '800px 0px 800px 0px' });
		sections.forEach(function (s) { observer.observe(s); });
	}

	function observeCursor() {
		if (cursorObserver) { cursorObserver.disconnect(); }
		if (!('IntersectionObserver' in window)) { return; }
		cursorObserver = new IntersectionObserver(function (entries) {
			entries.forEach(function (en) {
				if (!en.isIntersecting) { return; }
				setCursor(en.target.id.replace(/^y/, ''));
			});
		}, { rootMargin: '-200px 0px -70% 0px' });
		Array.prototype.forEach.call(el.content.querySelectorAll('h3.zl-year'), function (h) {
			if (/^y\d+$/.test(h.id)) { cursorObserver.observe(h); }
		});
	}

	function setCursor(year) {
		Array.prototype.forEach.call(el.axis.querySelectorAll('a'), function (a) {
			a.classList.toggle('current', a.dataset.year === year);
		});
		var i = +year - yearMin;
		if (el.cursor && i >= 0 && i < yearCount) {
			el.cursor.hidden = false;
			el.cursor.style.insetInlineStart = ((i + 0.5) / yearCount * 100) + '%';
		}
	}

	function undatedGroups(list, sections) {
		var head = document.createElement('section');
		head.className = 'zl-undated-head';
		head.appendChild(heading('y-undated', t().undated, list.length));
		el.content.appendChild(head);
		// undated pieces close the view, kept apart by lane
		LANES.forEach(function (lane) {
			var own = list.filter(function (e) { return e.lane === lane; });
			if (!own.length) { return; }
			var sec = group('y-undated-' + lane, t().lanes[lane], own);
			sec.classList.add('zl-undated');
			sections.push(sec);
		});
	}

	function appendPending(sections) {
		sections.forEach(function (s) {
			if (!s.parentNode) { el.content.appendChild(s); }
		});
	}

	function render() {
		var loc = state.lang;
		document.documentElement.lang = loc;
		document.body.classList.toggle('zl-compact', state.density === 'compact');
		el.title.firstChild.nodeValue = t().title + ' ';
		el.personLabel.textContent = t().person;
		el.person.placeholder = t().personHint;
		el.filterLabel.textContent = t().filters;
		if (el.person.value !== state.person) { el.person.value = state.person; }
		Array.prototype.forEach.call(document.querySelectorAll('[data-density]'), function (b) {
			b.setAttribute('aria-pressed', String(b.dataset.density === state.density));
			b.textContent = t()[b.dataset.density];
		});
		Array.prototype.forEach.call(document.querySelectorAll('[data-lang]'), function (b) {
			b.setAttribute('aria-pressed', String(b.dataset.lang === loc));
		});
		el.scale.setAttribute('aria-label', t().scale);

		buildLaneChips();
		buildPlaceSelect();
		buildActiveFilters();
		buildPersonList();
		buildScale();

		var shown = events.filter(function (e) { return matches(e); });
		el.content.innerHTML = '';
		var sections = [];
		var i = 0;
		while (i < shown.length && shown[i].year) {
			var year = shown[i].year;
			var list = [];
			while (i < shown.length && shown[i].year === year) { list.push(shown[i]); i++; }
			sections.push(group('y' + year, year, list));
		}
		sections.forEach(function (s) { el.content.appendChild(s); });
		var undated = shown.slice(i);
		if (undated.length) { undatedGroups(undated, sections); }
		appendPending(sections);
		if (!shown.length) {
			var p = document.createElement('p');
			p.className = 'zl-empty';
			p.textContent = t().empty;
			el.content.appendChild(p);
		}
		observeGroups(sections);
		observeCursor();
		writeUrl();
	}

	/* ---------- boot ---------- */

	function bind() {
		document.addEventListener('click', function (ev) {
			var b = ev.target.closest('[data-density],[data-lang]');
			if (b) {
				if (b.dataset.density) { state.density = b.dataset.density; }
				if (b.dataset.lang) { state.lang = b.dataset.lang; }
				render();
				return;
			}
			if (!el.placePopup.hidden && !ev.target.closest('#zl-place-select')) { closePlaces(); }
		});
		el.placeButton.addEventListener('click', function () {
			if (el.placePopup.hidden) { openPlaces(); } else { closePlaces(); }
		});
		el.placeSearch.addEventListener('input', buildPlaceSelect);
		el.placeSelect.addEventListener('keydown', function (ev) {
			if (ev.key !== 'Escape') { return; }
			closePlaces();
			el.placeButton.focus();
		});
		el.person.addEventListener('input', function () {
			state.person = el.person.value.trim();
			render();
		});
		el.filterToggle.addEventListener('click', function () {
			var collapsed = el.head.classList.toggle('zl-collapsed');
			el.filterToggle.setAttribute('aria-expanded', String(!collapsed));
		});
		// the copied navbar switches language by reloading the GAMS page; here the view
		// switches in place, so the inline handler gives way to the data attribute. The
		// navbar spans are no buttons, so they also get a role and keyboard handling.
		Array.prototype.forEach.call(document.querySelectorAll('[onclick*="jump_to_id_switching_language"]'), function (node) {
			var locale = /locale=en/.test(node.getAttribute('onclick')) ? 'en' : 'de';
			node.removeAttribute('onclick');
			node.dataset.lang = locale;
			node.setAttribute('role', 'button');
			node.setAttribute('tabindex', '0');
			node.addEventListener('keydown', function (ev) {
				if (ev.key !== 'Enter' && ev.key !== ' ') { return; }
				ev.preventDefault();
				node.click();
			});
		});
		bindScale();
	}

	window.szdZeitleiste = function (byLane) {
		el.head = document.getElementById('zl-head');
		el.title = document.getElementById('zl-title');
		el.lanes = document.getElementById('zl-lane-chips');
		el.active = document.getElementById('zl-active');
		el.placeSelect = document.getElementById('zl-place-select');
		el.placeButton = document.getElementById('zl-place-button');
		el.placePopup = document.getElementById('zl-place-popup');
		el.placeSearch = document.getElementById('zl-place-search');
		el.placeList = document.getElementById('zl-place-list');
		el.person = document.getElementById('zl-person');
		el.personLabel = document.getElementById('zl-person-label');
		el.personList = document.getElementById('zl-person-list');
		el.filterToggle = document.getElementById('zl-filter-toggle');
		el.filterLabel = document.getElementById('zl-filter-toggle-label');
		el.scale = document.getElementById('zl-scale');
		el.plot = document.getElementById('zl-plot');
		el.axis = document.getElementById('zl-axis');
		el.tip = document.getElementById('zl-tip');
		el.content = document.getElementById('zl-content');

		readUrl();
		events = prepare(byLane);
		var dated = events.filter(function (e) { return e.year; });
		yearMin = Math.min.apply(null, dated.map(function (e) { return +e.year; }));
		// the axis ends where the view ends, so the cut is visible instead of implied
		yearMax = MAX_YEAR;
		yearCount = yearMax - yearMin + 1;
		bind();
		render();
		if (document.location.hash) {
			var target = document.getElementById(document.location.hash.substring(1));
			if (target) { target.scrollIntoView(); }
		}
		return events.length;
	};

	function boot() {
		// resolved against the document, because <base> points at the live site
		var base = new URL('data/', document.location.href).href;
		Promise.all(LANES.map(function (lane) {
			return fetch(base + lane + '.json').then(function (r) { return r.json(); });
		})).then(function (parts) {
			var byLane = {};
			LANES.forEach(function (lane, i) { byLane[lane] = parts[i]; });
			window.szdZeitleiste(byLane);
		}).catch(function (err) {
			document.getElementById('zl-content').textContent = 'Lane-Dateien konnten nicht geladen werden: ' + err;
		});
	}

	if (typeof fetch === 'function' && document.location.protocol.indexOf('http') === 0) {
		if (document.readyState === 'loading') {
			document.addEventListener('DOMContentLoaded', boot);
		} else {
			boot();
		}
	}
})();
