/* The controls a comparison table grows past 8 rows.
   Search · sortable headers · per-column filters · dismissable pills · clear all.

   It reads the table that is already in the page. The data lives in the markup, so
   the page still reads with this file missing and nothing is written twice.

   Markup contract
     <div class="r-tablebox" data-report-table>
       <table class="r-table r-table-cards">
         <thead><tr>
           <th data-sort="text">Screen</th>          sortable, alphabetical
           <th data-sort="num" data-filter>Panel</th> sortable + filter menu
           <th>Verdict</th>                           neither
         </tr></thead>
         <tbody>
           <tr class="r-row-win"> … </tr>            the winner survives sorting
           <tr> <td data-label="Screen">…</td> … </tr>
         </tbody>
       </table>
     </div>

   Every <td> carries data-label so a phone can turn the row into a card.

   Two different keys, on purpose:
     data-value         what the column SORTS by — "120 Hz" sorts as 120
     data-filter-value  what the column FILTERS by — only when the cell's own
                        words are not the value. Otherwise the menu uses the
                        cell's words with any note under them stripped, so it
                        offers "120 Hz · not at all", never "0 · 60 · 100 · 120".  */

(function () {
  'use strict';

  /* The key a column SORTS by. A number cell carries data-value so "$1,499.99"
     sorts as 1499.99 and "120 Hz" sorts as 120. */
  function sortKey(td) {
    return (td.getAttribute('data-value') !== null ? td.getAttribute('data-value') : td.textContent)
      .trim();
  }

  /* The value a column FILTERS by — what the menu lists and what a pill says.
     Never the sort key: a menu offering "0 · 60 · 100 · 120" tells nobody what
     those numbers are. It is the cell's own words, minus any note under them.
     Override with data-filter-value when the cell's words are not the value. */
  function filterVal(td) {
    var explicit = td.getAttribute('data-filter-value');
    if (explicit !== null) return explicit.trim();
    var copy = td.cloneNode(true);
    [].forEach.call(copy.querySelectorAll('div,p,.r-small'), function (n) { n.remove(); });
    return copy.textContent.replace(/\s+/g, ' ').trim();
  }

  /* A heading's own words, without the sort arrow the script appended to it. */
  function headName(th) {
    var a = th.querySelector('.r-th-arrow');
    return th.textContent.replace(a ? a.textContent : '', '').replace(/\s+/g, ' ').trim();
  }

  /* A cell with no number is MISSING, not zero and not huge. Missing sinks to the
     bottom whichever way the column is sorted — a monitor with no price must never
     outrank one that actually costs $2,006. */
  function numOf(td) {
    var n = parseFloat(sortKey(td).replace(/[^0-9.\-]/g, ''));
    return isNaN(n) ? null : n;
  }

  function build(box) {
    var table = box.querySelector('table');
    if (!table) return;
    var heads = [].slice.call(table.tHead.rows[0].cells);
    var body = table.tBodies[0];
    var rows = [].slice.call(body.rows);
    if (!rows.length) return;

    var state = { q: '', sortCol: -1, dir: 1, filters: {} };
    /* The page names its own noun: <p data-report-count>45 monitors</p>. Read it once
       so the running count never says something the page does not call these things. */
    var counter = box.parentNode.querySelector('[data-report-count]');
    var noun = counter ? (counter.textContent.trim().replace(/^[\d,]+\s*/, '') || 'rows') : 'rows';
    table.classList.add('r-js');

    /* Lock the column widths the browser worked out for the FULL table, then switch to
       fixed layout. Sorting and filtering change which rows are visible, and with auto
       layout that re-measures every column and the whole table jumps sideways. Nothing
       may move except the rows.

       Measure LAST, not here. Two things widen a header after this point — the sort
       arrow appended to every sortable th, and the web font arriving to replace the
       fallback. Locking before either lands freezes columns too narrow for their own
       contents, and short cells wrap inside them: "Camp" breaking to "Cam / p" while
       "Club" in the same column fits. Caught on the Burning Man voice memo page,
       2026-09-07. The initial lock now runs at the foot of setup, after the arrows,
       and again once the font is ready. */
    window.addEventListener('resize', relock);
    var relockTimer;
    function relock() {
      clearTimeout(relockTimer);
      relockTimer = setTimeout(function () {
        table.style.tableLayout = 'auto';
        [].forEach.call(table.tHead.rows[0].cells, function (th) { th.style.width = ''; });
        lockColumns();
      }, 120);
    }
    /* A column may state its own width: <th data-w="9%">. Use it when it is given.
       One long prose column starves the short ones beside it — the browser hands the
       prose column the slack and leaves "Camp" a hair too narrow, so it wraps to
       "Cam / p". Measuring cannot fix that; only the author knows the column holds a
       word that must stay whole. Widths are shared out among the columns that do NOT
       declare one. */
    function lockColumns() {
      var wide = table.getBoundingClientRect().width;
      if (!wide) return;                       /* hidden or phone-card mode — nothing to lock */
      var declared = heads.map(function (th) { return th.getAttribute('data-w'); });
      var spoken = declared.reduce(function (sum, w) {
        return sum + (w ? parseFloat(w) : 0);
      }, 0);
      var free = heads.reduce(function (sum, th, i) {
        return sum + (declared[i] ? 0 : th.getBoundingClientRect().width);
      }, 0);
      heads.forEach(function (th, i) {
        if (declared[i]) { th.style.width = declared[i]; return; }
        var share = free ? th.getBoundingClientRect().width / free : 0;
        th.style.width = (share * (100 - spoken)).toFixed(4) + '%';
      });
      table.style.tableLayout = 'fixed';
    }

    /* --- controls ------------------------------------------------------- */
    var bar = document.createElement('div');
    bar.className = 'r-controls';

    var search = document.createElement('input');
    search.className = 'r-input';
    search.type = 'search';
    /* One word. A search box is the narrow case where the placeholder IS the label
       (`ux-no-narrating-copy`) — it never narrates beyond naming the control, and the
       row count already lives in the line above the table. */
    search.placeholder = 'Search';
    search.setAttribute('aria-label', 'Search the table');
    bar.appendChild(search);

    heads.forEach(function (th, i) {
      if (!th.hasAttribute('data-filter')) return;
      var values = [];
      rows.forEach(function (r) {
        var v = filterVal(r.cells[i]);
        if (v && values.indexOf(v) < 0) values.push(v);
      });
      values.sort();
      bar.appendChild(menu(headName(th), i, values));
    });

    var pills = document.createElement('div');
    pills.className = 'r-controls';
    pills.style.marginTop = '-4px';

    box.parentNode.insertBefore(bar, box);
    box.parentNode.insertBefore(pills, box);

    /* --- filter menu ---------------------------------------------------- */
    function menu(label, col, values) {
      var wrap = document.createElement('div');
      wrap.className = 'r-menu';
      var btn = document.createElement('button');
      btn.className = 'r-menu-btn';
      btn.type = 'button';
      btn.textContent = label;
      var panel = document.createElement('div');
      panel.className = 'r-menu-panel';
      panel.hidden = true;
      /* Ticking a box filters the table and leaves the menu open — you are almost
         always picking more than one. Only a click outside closes it. */
      panel.addEventListener('click', function (e) { e.stopPropagation(); });

      values.forEach(function (v) {
        var lab = document.createElement('label');
        var cb = document.createElement('input');
        cb.type = 'checkbox';
        cb.value = v;
        cb.setAttribute('data-col', col);
        cb.addEventListener('change', function () {
          var set = state.filters[col] || (state.filters[col] = []);
          var at = set.indexOf(v);
          if (cb.checked && at < 0) set.push(v);
          if (!cb.checked && at >= 0) set.splice(at, 1);
          render();
        });
        lab.appendChild(cb);
        lab.appendChild(document.createTextNode(v));
        panel.appendChild(lab);
      });

      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var open = panel.hidden;
        closeMenus();
        panel.hidden = !open;
        btn.setAttribute('aria-expanded', String(open));
      });
      wrap.appendChild(btn);
      wrap.appendChild(panel);
      return wrap;
    }

    function closeMenus() {
      [].forEach.call(document.querySelectorAll('.r-menu-panel'), function (p) { p.hidden = true; });
      [].forEach.call(document.querySelectorAll('.r-menu-btn'), function (b) {
        b.setAttribute('aria-expanded', 'false');
      });
    }
    document.addEventListener('click', closeMenus);

    /* --- sorting -------------------------------------------------------- */
    heads.forEach(function (th, i) {
      var kind = th.getAttribute('data-sort');
      if (!kind) return;
      th.classList.add('r-th-sort');
      th.tabIndex = 0;
      var arrow = document.createElement('span');
      arrow.className = 'r-th-arrow';
      th.appendChild(arrow);
      function go() {
        state.dir = state.sortCol === i ? -state.dir : (kind === 'num' ? -1 : 1);
        state.sortCol = i;
        render();
      }
      th.addEventListener('click', go);
      th.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); }
      });
    });

    search.addEventListener('input', function () { state.q = search.value.trim().toLowerCase(); render(); });

    /* --- render --------------------------------------------------------- */
    function render() {
      var shown = rows.filter(function (r) {
        for (var col in state.filters) {
          var set = state.filters[col];
          if (set.length && set.indexOf(filterVal(r.cells[col])) < 0) return false;
        }
        return !state.q || r.textContent.toLowerCase().indexOf(state.q) >= 0;
      });

      if (state.sortCol >= 0) {
        var col = state.sortCol;
        var kind = heads[col].getAttribute('data-sort');
        shown = shown.slice().sort(function (a, b) {
          if (kind === 'num') {
            var x = numOf(a.cells[col]), y = numOf(b.cells[col]);
            if (x === null && y === null) return 0;
            if (x === null) return 1;             /* missing always last */
            if (y === null) return -1;
            return (x - y) * state.dir;
          }
          return sortKey(a.cells[col]).localeCompare(sortKey(b.cells[col])) * state.dir;
        });
      }

      rows.forEach(function (r) { r.hidden = true; });
      shown.forEach(function (r, i) {
        r.hidden = false;
        r.classList.toggle('r-band', i % 2 === 1 && !r.classList.contains('r-row-win'));
        body.appendChild(r);
      });

      heads.forEach(function (th, i) {
        var a = th.querySelector('.r-th-arrow');
        if (a) a.textContent = state.sortCol === i ? (state.dir === 1 ? ' ▲' : ' ▼') : '';
      });

      /* pills — one per active filter, plus clear all at two or more */
      pills.textContent = '';
      var active = [];
      Object.keys(state.filters).forEach(function (col) {
        state.filters[col].forEach(function (v) {
          active.push({ col: col, v: v, label: headName(heads[col]).toLowerCase() + ' — ' + v });
        });
      });
      active.forEach(function (f) {
        var pill = document.createElement('span');
        pill.className = 'r-pill';
        pill.appendChild(document.createTextNode(f.label));
        var x = document.createElement('button');
        x.type = 'button';
        x.textContent = '×';
        x.setAttribute('aria-label', 'Remove filter ' + f.label);
        x.addEventListener('click', function () {
          var set = state.filters[f.col];
          set.splice(set.indexOf(f.v), 1);
          syncBoxes();
          render();
        });
        pill.appendChild(x);
        pills.appendChild(pill);
      });
      if (active.length > 1) {
        var clear = document.createElement('button');
        clear.type = 'button';
        clear.className = 'r-clear';
        clear.textContent = 'clear all';
        clear.addEventListener('click', function () {
          state.filters = {};
          syncBoxes();
          render();
        });
        pills.appendChild(clear);
      }

      if (counter) {
        counter.textContent = shown.length === rows.length
          ? rows.length + ' ' + noun
          : shown.length + ' of ' + rows.length + ' ' + noun;
      }
    }

    function syncBoxes() {
      [].forEach.call(bar.querySelectorAll('input[type=checkbox]'), function (cb) {
        var set = state.filters[cb.getAttribute('data-col')] || [];
        cb.checked = set.indexOf(cb.value) >= 0;
      });
    }

    render();

    /* Now everything that can change a column's width is in place — the sort arrows,
       the controls bar, the first render. Measure and freeze here, then once more when
       the web font lands. */
    lockColumns();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(relock);
  }

  function init() {
    [].forEach.call(document.querySelectorAll('[data-report-table]'), build);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
