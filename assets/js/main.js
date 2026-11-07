/* Material Lab — site behaviour (no dependencies) */
document.addEventListener('DOMContentLoaded', function () {
  var qsa = function (sel, root) { return [].slice.call((root || document).querySelectorAll(sel)); };

  // ---- Language helpers (strings come from _data/i18n.yml via window.LAB_I18N) ----
  var I18N = window.LAB_I18N || {};
  var lang = function () { return document.documentElement.lang === 'id' ? 'id' : 'en'; };
  var tr = function (key) { var v = I18N[key]; return v ? (v[lang()] || v.en) : key; };

  // ---- Mobile navigation ----
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var expanded = this.getAttribute('aria-expanded') === 'true';
      this.setAttribute('aria-expanded', String(!expanded));
      links.classList.toggle('open');
    });
    document.addEventListener('click', function (e) {
      if (!e.target.closest('.site-nav') && links.classList.contains('open')) {
        toggle.setAttribute('aria-expanded', 'false');
        links.classList.remove('open');
      }
    });
  }

  // ---- Dropdown menus ----
  var closeDropdowns = function (except) {
    qsa('.nav-dropdown__toggle').forEach(function (btn) {
      if (btn === except) return;
      btn.setAttribute('aria-expanded', 'false');
      if (btn.nextElementSibling) btn.nextElementSibling.classList.remove('open');
    });
  };
  qsa('.nav-dropdown__toggle').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var expanded = this.getAttribute('aria-expanded') === 'true';
      closeDropdowns(btn);
      this.setAttribute('aria-expanded', String(!expanded));
      if (this.nextElementSibling) this.nextElementSibling.classList.toggle('open');
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav-dropdown')) closeDropdowns(null);
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeDropdowns(null); });

  // ---- Publication filters: theme + year + search, all combinable; long list shows 10 first ----
  var pubFilters = document.getElementById('pubFilters');
  if (pubFilters) {
    var PUB_LIMIT = 10;
    var pubClear = document.getElementById('pubClear');
    var pubEmpty = document.getElementById('pubEmpty');
    var pubSearch = document.getElementById('pubSearch');
    var pubYear = document.getElementById('pubYear');
    var pubCount = document.getElementById('pubCount');
    var pubMore = document.getElementById('pubMore');
    var pubItems = qsa('.pub-item');
    var pubText = pubItems.map(function (el) { return el.textContent.toLowerCase(); });
    var activeTheme = null, activeYear = null, query = '', expanded = false;

    var apply = function () {
      var filtered = activeTheme !== null || activeYear !== null || query !== '';
      var shown = 0, visible = 0;
      pubItems.forEach(function (item, i) {
        var match = (activeTheme === null || item.dataset.theme === activeTheme) &&
                    (activeYear === null || item.dataset.year === activeYear) &&
                    (query === '' || pubText[i].indexOf(query) !== -1);
        var show = match && (filtered || expanded || shown < PUB_LIMIT);
        item.style.display = show ? '' : 'none';
        if (match) shown++;
        if (show) visible++;
      });
      qsa('.pub-filter-theme', pubFilters).forEach(function (b) { b.classList.toggle('active', b.dataset.theme === activeTheme); });
      if (pubYear) pubYear.value = activeYear === null ? '' : activeYear;
      if (pubClear) pubClear.hidden = !filtered;
      if (pubEmpty) pubEmpty.hidden = shown > 0;
      if (pubMore) {
        pubMore.hidden = filtered || pubItems.length <= PUB_LIMIT;
        pubMore.textContent = expanded ? tr('show_less') : tr('pub_more') + ' (' + (pubItems.length - PUB_LIMIT) + ')';
      }
      if (pubCount) pubCount.textContent = filtered
        ? shown + ' ' + tr('js_of') + ' ' + pubItems.length + ' ' + tr('js_publications')
        : pubItems.length + ' ' + tr('js_publications');
    };

    if (pubSearch) pubSearch.addEventListener('input', function () { query = this.value.trim().toLowerCase(); apply(); });
    if (pubYear) pubYear.addEventListener('change', function () { activeYear = this.value === '' ? null : this.value; apply(); });
    if (pubMore) pubMore.addEventListener('click', function () { expanded = !expanded; apply(); });
    pubFilters.addEventListener('click', function (e) {
      var btn = e.target.closest('.pub-filter-btn');
      if (!btn) return;
      if (btn === pubClear) {
        activeTheme = null; activeYear = null; query = '';
        if (pubSearch) pubSearch.value = '';
      } else if (btn.dataset.theme !== undefined) {
        activeTheme = activeTheme === btn.dataset.theme ? null : btn.dataset.theme;
      }
      apply();
    });
    qsa('.pub-theme').forEach(function (pill) {
      pill.addEventListener('click', function () {
        activeTheme = activeTheme === this.dataset.theme ? null : this.dataset.theme;
        apply();
        pubFilters.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
    apply();
    document.addEventListener('langchange', apply);
  }

  // ---- Calendar: mark past items and show days remaining ----
  var deadlineItems = qsa('.deadline-item');
  var renderDeadlines = function () {
    deadlineItems.forEach(function (item) {
      var parts = (item.dataset.date || '').split('-');
      if (parts.length !== 3) return;
      var due = new Date(+parts[0], +parts[1] - 1, +parts[2]);
      var today = new Date(); today.setHours(0, 0, 0, 0);
      var days = Math.round((due - today) / 86400000);
      var label = item.querySelector('.deadline-count');
      if (days < 0) { item.classList.add('is-past'); if (label) label.textContent = tr('js_passed'); }
      else if (label) {
        label.textContent = days === 0 ? tr('js_today')
          : (lang() === 'id' ? days + ' ' + tr('js_days_left') : days + ' ' + tr(days === 1 ? 'js_day_left' : 'js_days_left'));
      }
    });
  };
  document.addEventListener('langchange', renderDeadlines);

  // ---- Project videos: load and play only while visible ----
  var videos = qsa('.project-video');
  if (videos.length && 'IntersectionObserver' in window) {
    var vObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var v = entry.target;
        if (entry.isIntersecting) {
          if (!v.src && v.dataset.src) v.src = v.dataset.src;
          var p = v.play(); if (p && p.catch) p.catch(function () {});
        } else { v.pause(); }
      });
    }, { threshold: 0.25 });
    videos.forEach(function (v) { vObs.observe(v); });
  }

  // ---- Grants: filter by status ----
  var grantFilters = document.getElementById('grantFilters');
  if (grantFilters) {
    var grantCards = qsa('.grant-card');
    var grantCount = document.getElementById('grantCount');
    var grantEmpty = document.getElementById('grantEmpty');
    var grantStatus = 'all';
    var applyGrants = function () {
      var shown = 0;
      grantCards.forEach(function (c) {
        var ok = grantStatus === 'all' || c.dataset.status === grantStatus;
        c.style.display = ok ? '' : 'none';
        if (ok) shown++;
      });
      qsa('.grant-filter-btn', grantFilters).forEach(function (b) { b.classList.toggle('active', b.dataset.status === grantStatus); });
      if (grantCount) grantCount.textContent = shown + ' ' + tr('js_grants');
      if (grantEmpty) grantEmpty.hidden = shown > 0;
    };
    grantFilters.addEventListener('click', function (e) {
      var btn = e.target.closest('.grant-filter-btn');
      if (!btn) return;
      grantStatus = btn.dataset.status;
      applyGrants();
    });
    document.addEventListener('langchange', applyGrants);
    applyGrants();
  }

  // ---- Grants total: count-up and live USD/IDR rate (falls back to the reference rate in _config.yml) ----
  var gt = document.getElementById('grantTotal'), hs = document.getElementById('hsUsd'), host = gt || hs;   // Grants page card, or the Home hero figure
  if (host) {
    var total = parseFloat(host.getAttribute('data-total')) || 0;
    var elIdr = document.getElementById('gtIdr'), elUsd = document.getElementById('gtUsd'), elRate = document.getElementById('gtRate');
    var rate = parseFloat(host.getAttribute('data-rate')) || 0, rateDate = host.getAttribute('data-rate-date') || '', live = false, rateTime = false;
    var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var fmtNum = function (n) { return Math.round(n).toLocaleString(lang() === 'id' ? 'id-ID' : 'en-US'); };
    var fmtRp = function (n) { return Math.round(n).toLocaleString('id-ID'); };   // Rupiah always with dots, as on the rest of the site
    var shown = { idr: total, usd: rate ? total / rate : 0 };
    // short form for the Home figure: 842 / 42K / 1.2M (same number as the Grants card, only rounded for display)
    var fmtShort = function (n) {
      if (n >= 999500) { var m = (Math.round(n / 1e5) / 10).toString(); return (lang() === 'id' ? m.replace('.', ',') : m) + 'M'; }
      if (n >= 1000) return Math.round(n / 1000) + 'K';
      return Math.round(n).toString();
    };
    var paint = function () {
      if (gt) {
        elIdr.textContent = 'Rp ' + fmtRp(shown.idr);
        elUsd.textContent = rate ? 'US$ ' + fmtNum(shown.usd) : '';
      }
      if (hs && rate) hs.textContent = fmtShort(shown.usd);
    };
    var note = function () {
      if (!elRate) return;
      if (!rate) { elRate.textContent = ''; return; }
      var d = rateDate;
      try {
        if (rateTime) d = new Date(d).toLocaleString(lang() === 'id' ? 'id-ID' : 'en-GB', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
        else if (/^\d{4}-\d{2}-\d{2}/.test(d)) d = new Date(d.slice(0, 10) + 'T00:00:00Z').toLocaleDateString(lang() === 'id' ? 'id-ID' : 'en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' });
      } catch (e) {}
      elRate.textContent = tr(live ? 'js_rate_live' : 'js_rate_ref').replace('{rate}', fmtRp(rate)).replace('{date}', d);
    };
    var animate = function (from, to, ms, done) {
      if (calm || !window.requestAnimationFrame) { done(to); return; }
      var t0 = null;
      var step = function (t) {
        if (t0 === null) t0 = t;
        var k = Math.min(1, (t - t0) / ms), e = 1 - Math.pow(1 - k, 3);
        done(from + (to - from) * e);
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    var fetchJson = function (url) {
      return new Promise(function (ok, no) {
        var c = window.AbortController ? new AbortController() : null;
        var timer = setTimeout(function () { if (c) c.abort(); no(new Error('timeout')); }, 4500);
        fetch(url, c ? { signal: c.signal } : {}).then(function (r) { return r.json(); }).then(function (j) { clearTimeout(timer); ok(j); }, function (e) { clearTimeout(timer); no(e); });
      });
    };
    var parseNum = function (t) {
      t = String(t || '').replace(/["\s]/g, '').replace(/^Rp/i, '');
      var lc = t.lastIndexOf(','), ld = t.lastIndexOf('.');
      if (lc > -1 && ld > -1) t = lc > ld ? t.replace(/\./g, '').replace(',', '.') : t.replace(/,/g, '');
      else if (lc > -1) t = /,\d{1,2}$/.test(t) ? t.replace(',', '.') : t.replace(/,/g, '');
      else if (ld > -1 && /\.\d{3}(\.|$)/.test(t) && t.split('.').length > 2) t = t.replace(/\./g, '');
      return parseFloat(t);
    };
    var sheetUrl = host.getAttribute('data-sheet') || '';
    var getSheetRate = function () {
      var c = window.AbortController ? new AbortController() : null;
      var timer = setTimeout(function () { if (c) c.abort(); }, 4500);
      return fetch(sheetUrl + (sheetUrl.indexOf('?') > -1 ? '&' : '?') + 't=' + Date.now(), { cache: 'no-store', signal: c ? c.signal : undefined })
        .then(function (r) { clearTimeout(timer); return r.text(); })
        .then(function (txt) {
          var row = txt.split(/\r?\n/)[0].match(/("([^"]*)"|[^,]+)/g) || [];
          var v = parseNum(row[0]);
          if (!(v > 1000 && v < 100000)) throw new Error('bad');
          var when = String(row[1] || '').replace(/"/g, '').trim();
          var d = new Date(when);
          return { rate: v, date: isNaN(d) ? new Date().toISOString() : d.toISOString(), time: true };
        });
    };
    var getRate = function () {
      if (!window.fetch || !window.Promise) return Promise.reject(new Error('unsupported'));
      if (sheetUrl) return getSheetRate().catch(function () { return getPublicRate(); });
      return getPublicRate();
    };
    var getPublicRate = function () {
      return fetchJson('https://api.frankfurter.dev/v1/latest?base=USD&symbols=IDR').then(function (j) {
        if (!j || !j.rates || !j.rates.IDR) throw new Error('bad');
        return { rate: j.rates.IDR, date: j.date };
      }).catch(function () {
        return fetchJson('https://open.er-api.com/v6/latest/USD').then(function (j) {
          if (!j || !j.rates || !j.rates.IDR) throw new Error('bad');
          return { rate: j.rates.IDR, date: (j.time_last_update_utc ? new Date(j.time_last_update_utc).toISOString() : '') };
        });
      });
    };
    if (gt) { shown.idr = 0; shown.usd = 0; paint(); note(); }
    var ratePromise = getRate().then(function (r) {
      if (r.rate > 1000 && r.rate < 100000) { rate = r.rate; rateDate = r.date || rateDate; rateTime = !!r.time; live = true; }
    }, function () {}).then(function () { note(); });
    var run = function () {
      ratePromise.then(function () {
        var usdTo = rate ? total / rate : 0;
        animate(0, total, 1600, function (v) { shown.idr = v; shown.usd = rate ? v / total * usdTo : 0; paint(); });
      });
    };
    if ('IntersectionObserver' in window && !calm) {
      var o2 = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { o2.disconnect(); run(); } }, { threshold: .4 });
      o2.observe(host);
    } else { run(); }
    document.addEventListener('langchange', function () { paint(); note(); });
    new MutationObserver(function () { paint(); note(); }).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  }

  // ---- Count-up for the small statistic numbers (Home hero, About, Grants); the HTML already holds the final number ----
  var statEls = qsa('.hero-stats b, .grant-stat-num').filter(function (el) { return /^\d+$/.test(el.textContent.trim()); });
  var calmStats = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (statEls.length && 'IntersectionObserver' in window && window.requestAnimationFrame && !calmStats) {
    var countUp = function (el) {
      var to = parseInt(el.textContent, 10), t0 = null;
      el.style.minWidth = el.offsetWidth + 'px';
      var step = function (t) {
        if (t0 === null) t0 = t;
        var k = Math.min(1, (t - t0) / 1200);
        el.textContent = Math.round(to * (1 - Math.pow(1 - k, 3)));
        if (k < 1) requestAnimationFrame(step);
      };
      el.textContent = '0';
      requestAnimationFrame(step);
    };
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { so.unobserve(en.target); countUp(en.target); } });
    }, { threshold: .6 });
    statEls.forEach(function (el) { so.observe(el); });
  }


  // ---- Motion polish (desktop pointer effects, scroll progress); every effect is off for "reduce motion" ----
  var calmM = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePtr = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (!calmM) {
    // thin progress bar at the top while scrolling
    var bar = document.createElement('div');
    bar.className = 'scroll-bar'; bar.setAttribute('aria-hidden', 'true');
    document.body.appendChild(bar);
    var barTick = false;
    var barDraw = function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, window.pageYOffset / h) : 0) + ')';
      barTick = false;
    };
    window.addEventListener('scroll', function () { if (!barTick) { barTick = true; requestAnimationFrame(barDraw); } }, { passive: true });
    barDraw();
  }
  if (!calmM && finePtr) {
    // hero: the isometric scene and the hexagon pattern shift a little in opposite directions with the pointer
    var heroWrap = document.querySelector('.hero-wrap');
    var heroVis = document.querySelector('.hero--iso .hero-visual');
    if (heroWrap && heroVis) {
      var hTick = false, hx = 0, hy = 0;
      var hDraw = function () {
        heroWrap.style.setProperty('--hx', (hx * -14).toFixed(1) + 'px');
        heroWrap.style.setProperty('--hy', (hy * -10).toFixed(1) + 'px');
        heroVis.style.setProperty('--vx', (hx * 10).toFixed(1) + 'px');
        heroVis.style.setProperty('--vy', (hy * 7).toFixed(1) + 'px');
        heroVis.style.setProperty('--ry', (hx * 2.2).toFixed(2) + 'deg');
        heroVis.style.setProperty('--rx', (hy * -1.6).toFixed(2) + 'deg');
        hTick = false;
      };
      heroWrap.addEventListener('pointermove', function (e) {
        var r = heroWrap.getBoundingClientRect();
        hx = ((e.clientX - r.left) / r.width - .5) * 2; hy = ((e.clientY - r.top) / r.height - .5) * 2;
        if (!hTick) { hTick = true; requestAnimationFrame(hDraw); }
      });
      heroWrap.addEventListener('pointerleave', function () { hx = 0; hy = 0; requestAnimationFrame(hDraw); });
    }
    // cards: gentle 3D tilt and a soft yellow glow that follows the pointer
    qsa('.blog-card, .project-card:not(.project-card--open), .grant-card, .team-member').forEach(function (card) {
      card.classList.add('tilt');
      var tTick = false, ev = null;
      var tDraw = function () {
        if (!ev) { tTick = false; return; }
        var r = card.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width, y = (ev.clientY - r.top) / r.height;
        card.style.setProperty('--ry', ((x - .5) * 3).toFixed(2) + 'deg');
        card.style.setProperty('--rx', ((.5 - y) * 2.4).toFixed(2) + 'deg');
        card.style.setProperty('--mx', (x * 100).toFixed(0) + '%');
        card.style.setProperty('--my', (y * 100).toFixed(0) + '%');
        tTick = false;
      };
      card.addEventListener('pointermove', function (e) { ev = e; if (!tTick) { tTick = true; requestAnimationFrame(tDraw); } });
      card.addEventListener('pointerleave', function () { ev = null; card.style.removeProperty('--ry'); card.style.removeProperty('--rx'); });
    });
    // primary buttons lean slightly toward the pointer
    qsa('.btn-primary, .btn-outline').forEach(function (b) {
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        b.style.setProperty('--bx', ((e.clientX - r.left) / r.width - .5) * 6 + 'px');
        b.style.setProperty('--by', ((e.clientY - r.top) / r.height - .5) * 4 + 'px');
      });
      b.addEventListener('pointerleave', function () { b.style.removeProperty('--bx'); b.style.removeProperty('--by'); });
    });
  }

  // ---- From plant to product (Home): selectable steps, auto-advance until the visitor interacts ----
  var flow = document.getElementById('flowMap');
  if (flow) {
    var fNodes = qsa('.flow-node', flow), fPanels = qsa('.flow-panel', flow), fFill = document.getElementById('flowFill');
    var fCur = 0, fAuto = null, fTouched = false;
    var fSet = function (i) {
      fCur = (i + fNodes.length) % fNodes.length;
      fNodes.forEach(function (n, k) {
        n.classList.toggle('is-active', k === fCur); n.classList.toggle('is-done', k < fCur);
        n.setAttribute('aria-selected', k === fCur ? 'true' : 'false'); n.setAttribute('tabindex', k === fCur ? '0' : '-1');
      });
      fPanels.forEach(function (p, k) { p.classList.toggle('is-active', k === fCur); });
      flow.style.setProperty('--p', fCur / (fNodes.length - 1));
    };
    var fStop = function () { fTouched = true; if (fAuto) { clearInterval(fAuto); fAuto = null; } };
    fNodes.forEach(function (n, k) {
      n.addEventListener('click', function () { fStop(); fSet(k); });
      n.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (d) { e.preventDefault(); fStop(); fSet(fCur + d); fNodes[fCur].focus(); }
      });
    });
    flow.addEventListener('pointerenter', function () { if (fAuto) { clearInterval(fAuto); fAuto = null; } });
    fSet(0);
    var calmF = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!calmF && 'IntersectionObserver' in window) {
      var fStart = function () { if (!fTouched && !fAuto) fAuto = setInterval(function () { fSet(fCur + 1); }, 4500); };
      new IntersectionObserver(function (en) {
        if (en[0].isIntersecting) fStart(); else if (fAuto) { clearInterval(fAuto); fAuto = null; }
      }, { threshold: .5 }).observe(flow);
      flow.addEventListener('pointerleave', function () { if (!fTouched) fStart(); });
    }
  }

  // ---- Site search (Ctrl/Cmd+K, "/" or the magnifier): the index loads only when the box is first opened ----
  var sIndex = null, sBox = null, sInput, sList, sSel = 0, sHits = [];
  var sNorm = function (t) { return String(t || '').toLowerCase(); };
  var sBuild = function () {
    sBox = document.createElement('div');
    sBox.className = 'search-modal'; sBox.hidden = true;
    sBox.innerHTML = '<div class="search-backdrop" data-search-close></div><div class="search-panel" role="dialog" aria-modal="true" aria-label="' + tr('search_open') + '">' +
      '<div class="search-field"><i class="fas fa-magnifying-glass" aria-hidden="true"></i><input type="search" autocomplete="off" spellcheck="false" aria-label="' + tr('search_open') + '"><kbd>Esc</kbd></div>' +
      '<ul class="search-list" role="listbox"></ul><p class="search-hint"></p></div>';
    document.body.appendChild(sBox);
    sInput = sBox.querySelector('input'); sList = sBox.querySelector('.search-list');
    sBox.addEventListener('click', function (e) { if (e.target.hasAttribute('data-search-close')) sClose(); });
    sInput.addEventListener('input', sRun);
    sInput.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault(); if (!sHits.length) return;
        sSel = (sSel + (e.key === 'ArrowDown' ? 1 : -1) + sHits.length) % sHits.length; sPaint();
      } else if (e.key === 'Enter') {
        if (sHits[sSel]) { window.location.href = sHits[sSel].u; }
      }
    });
  };
  var sPaint = function () {
    var L = lang();
    sList.innerHTML = '';
    if (!sInput.value.trim()) { sBox.querySelector('.search-hint').textContent = tr('search_hint'); return; }
    sBox.querySelector('.search-hint').textContent = sHits.length ? '' : tr('search_none');
    sHits.forEach(function (h, i) {
      var li = document.createElement('li');
      li.setAttribute('role', 'option');
      if (i === sSel) li.className = 'is-sel';
      var a = document.createElement('a'); a.href = h.u;
      if (/^https?:/.test(h.u)) { a.target = '_blank'; a.rel = 'noopener'; }
      var tag = document.createElement('span'); tag.className = 'search-tag'; tag.textContent = tr('search_type_' + h.t);
      var ti = document.createElement('span'); ti.className = 'search-title'; ti.textContent = L === 'id' ? h.b : h.a;
      a.appendChild(tag); a.appendChild(ti); li.appendChild(a);
      a.addEventListener('mousemove', function () { sSel = i; var s = sList.querySelector('.is-sel'); if (s) s.classList.remove('is-sel'); li.classList.add('is-sel'); });
      sList.appendChild(li);
    });
    var cur = sList.querySelector('.is-sel'); if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: 'nearest' });
  };
  var sRun = function () {
    var q = sNorm(sInput.value).trim();
    sSel = 0; sHits = [];
    if (q && sIndex) {
      var toks = q.split(/\s+/);
      sIndex.forEach(function (it) {
        var ti = sNorm(it.a + ' ' + it.b), tx = sNorm(it.x), sc = 0, ok = true;
        toks.forEach(function (w) {
          if (ti.indexOf(w) !== -1) sc += 3 + (ti.indexOf(w) === 0 ? 1 : 0); else if (tx.indexOf(w) !== -1) sc += 1; else ok = false;
        });
        if (ok) { var o = { t: it.t, a: it.a, b: it.b, u: it.u, s: sc }; sHits.push(o); }
      });
      sHits.sort(function (x, y) { return y.s - x.s; }); sHits = sHits.slice(0, 8);
    }
    sPaint();
  };
  var sClose = function () { if (sBox) { sBox.hidden = true; document.documentElement.classList.remove('search-open'); } };
  var sOpen = function () {
    if (!sBox) sBuild();
    sBox.hidden = false; document.documentElement.classList.add('search-open');
    sInput.placeholder = tr('search_site_placeholder'); sInput.value = ''; sHits = []; sPaint(); sInput.focus();
    if (!sIndex && window.fetch && window.LAB_SEARCH) {
      fetch(window.LAB_SEARCH).then(function (r) { return r.json(); }).then(function (j) { sIndex = j; sRun(); }).catch(function () {});
    }
  };
  qsa('[data-search-open]').forEach(function (b) { b.addEventListener('click', function () { sOpen(); }); });
  document.addEventListener('keydown', function (e) {
    var typing = /^(INPUT|TEXTAREA|SELECT)$/.test((document.activeElement || {}).tagName || '');
    if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) { e.preventDefault(); sOpen(); }
    else if (e.key === '/' && !typing && !(sBox && !sBox.hidden)) { e.preventDefault(); sOpen(); }
    else if (e.key === 'Escape' && sBox && !sBox.hidden) { sClose(); }
  });
  // a search link from the site search can open Publications with the text already in the filter box
  (function () {
    var box = document.getElementById('pubSearch');
    var m = /[?&]q=([^&]*)/.exec(window.location.search);
    if (box && m) { try { box.value = decodeURIComponent(m[1].replace(/\+/g, ' ')); box.dispatchEvent(new Event('input')); } catch (e) {} }
  })();

  // ---- Publications charts: a bar filters the list below ----
  qsa('.pub-charts .bar-v').forEach(function (b) {
    b.addEventListener('click', function () {
      var sel = document.getElementById('pubYear'); if (!sel) return;
      sel.value = sel.value === b.getAttribute('data-year') ? '' : b.getAttribute('data-year');
      sel.dispatchEvent(new Event('change'));
      var f = document.getElementById('pubFilters'); if (f) f.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
  qsa('.pub-charts .bar-h').forEach(function (b) {
    b.addEventListener('click', function () {
      var btn = document.querySelector('.pub-filter-theme[data-theme="' + b.getAttribute('data-theme') + '"]');
      if (btn) btn.click();
      var f = document.getElementById('pubFilters'); if (f) f.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  // ---- Hero title: one highlighted word is typed, deleted and replaced by the next (loops while the hero is visible) ----
  var typerLive = null;
  var typerStart = function () {
    if (typerLive) { typerLive.stop(); typerLive = null; }
    var h1 = document.querySelector('.hero-title');
    var el = h1 && qsa('.typer', h1).filter(function (e) { return e.offsetParent !== null; })[0];
    if (!el) return;
    var words = (el.getAttribute('data-words') || '').split('|').filter(Boolean);
    if (words.length < 2) return;
    // reserve the tallest wrapped height so nothing below the title jumps while the word changes
    var lockHeight = function () {
      var keep = el.textContent, max = 0;
      h1.style.minHeight = '';
      words.forEach(function (w) { el.textContent = w; max = Math.max(max, h1.offsetHeight); });
      el.textContent = keep; h1.style.minHeight = max + 'px';
    };
    var calmT = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    el.textContent = words[0];
    lockHeight();
    if (calmT) return;
    var timer = null, running = false, wi = 0, ci = words[0].length, phase = 'hold', seen = true;
    el.classList.add('is-typing');
    var tick = function () {
      if (!running) return;
      var w = words[wi], d = 90;
      if (phase === 'hold') { phase = 'del'; d = 1900; }
      else if (phase === 'del') {
        ci--; el.textContent = w.slice(0, ci); d = 42;
        if (ci <= 0) { wi = (wi + 1) % words.length; phase = 'type'; d = 280; }
      } else {
        ci++; el.textContent = words[wi].slice(0, ci); d = 85;
        if (ci >= words[wi].length) { phase = 'hold'; d = 0; }
      }
      timer = setTimeout(tick, d);
    };
    var go = function () { if (!running && seen && !document.hidden) { running = true; timer = setTimeout(tick, 1500); } };
    var halt = function () { running = false; if (timer) { clearTimeout(timer); timer = null; } };
    var vis = function () { if (document.hidden) halt(); else go(); };
    document.addEventListener('visibilitychange', vis);
    var onResize = function () { var keep = el.textContent; lockHeight(); el.textContent = keep; };
    window.addEventListener('resize', onResize);
    var io = null;
    if ('IntersectionObserver' in window) {
      io = new IntersectionObserver(function (en) { seen = en[0].isIntersecting; if (seen) go(); else halt(); }, { threshold: .1 });
      io.observe(h1);
    }
    go();
    typerLive = { stop: function () {
      halt(); document.removeEventListener('visibilitychange', vis); window.removeEventListener('resize', onResize);
      if (io) io.disconnect(); el.classList.remove('is-typing'); el.textContent = words[0]; h1.style.minHeight = '';
    } };
  };
  typerStart();
  new MutationObserver(function () { setTimeout(typerStart, 0); }).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });

  // ---- Email links: also copy the address and show it, because mailto does nothing without a mail app ----
  var toastEl = null, toastTimer = null;
  var showToast = function (text) {
    if (!toastEl) { toastEl = document.createElement('div'); toastEl.className = 'toast'; toastEl.setAttribute('role', 'status'); toastEl.setAttribute('aria-live', 'polite'); document.body.appendChild(toastEl); }
    toastEl.textContent = text; toastEl.classList.add('show');
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { toastEl.classList.remove('show'); }, 2800);
  };
  var copyText = function (text) {
    if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(text);
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea'); ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.top = '0'; ta.style.left = '-9999px';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy') ? resolve() : reject(); } catch (e) { reject(e); } document.body.removeChild(ta);
    });
  };
  qsa('a[href^="mailto:"]').forEach(function (a) {
    var addr = a.getAttribute('href').replace(/^mailto:/, '').split('?')[0];
    a.addEventListener('click', function () {
      copyText(addr).then(function () { showToast(addr + ' ' + tr('copied')); }, function () { showToast(addr); });
    });
  });

  // ---- Contact form (Web3Forms, no backend of our own) ----
  var cForm = document.getElementById('contactForm');
  var cStatus = document.getElementById('cfStatus');
  var cStatusKey = null;
  var showStatus = function (key, cls) {
    if (!cStatus) return;
    cStatusKey = key;
    cStatus.className = 'form-status' + (cls ? ' ' + cls : '');
    cStatus.textContent = '';
    if (!key) return;
    cStatus.appendChild(document.createTextNode(tr(key) + (key === 'form_err' ? ' ' : '')));
    if (key === 'form_err') {
      var a = document.createElement('a'); a.href = 'mailto:' + cForm.dataset.mail; a.textContent = cForm.dataset.mail;
      cStatus.appendChild(a);
    }
  };
  if (cForm) {
    var cSend = document.getElementById('cfSend');
    cForm.dataset.mail = (document.querySelector('.contact-primary-email') || {}).textContent || '';
    cForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!cForm.checkValidity()) { cForm.reportValidity(); return; }
      var body = {};
      [].slice.call(cForm.elements).forEach(function (el) {
        if (!el.name || el.type === 'submit') return;
        body[el.name] = el.type === 'checkbox' ? (el.checked ? 'on' : '') : el.value;
      });
      body.subject = 'Website inquiry - ' + body.topic;
      body.language = lang();
      cSend.disabled = true; showStatus('form_sending', '');
      fetch(cForm.action, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(body) })
        .then(function (r) { return r.json(); })
        .then(function (j) { if (!j.success) throw new Error(j.message || 'failed'); cForm.reset(); showStatus('form_ok', 'is-ok'); })
        .catch(function () { showStatus('form_err', 'is-error'); })
        .then(function () { cSend.disabled = false; });
    });
  }

  // ---- Language switch (EN | ID); the choice is remembered in this browser ----
  var syncLang = function () {
    qsa('.lang-btn').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.setLang === lang())); });
    var search = document.getElementById('pubSearch');
    if (search) { search.placeholder = tr('search_placeholder'); search.setAttribute('aria-label', tr('search_placeholder')); }
    var yearSel = document.getElementById('pubYear');
    if (yearSel) { yearSel.options[0].textContent = tr('year_all'); yearSel.setAttribute('aria-label', tr('year_filter')); }
    qsa('[data-ph]').forEach(function (el) { el.placeholder = tr(el.dataset.ph); });
    qsa('[data-opt]').forEach(function (el) { el.textContent = tr(el.dataset.opt); });
    var sendLbl = document.getElementById('cfSendLabel'); if (sendLbl) sendLbl.textContent = tr('form_send');
    if (cStatusKey) showStatus(cStatusKey, cStatus.className.replace('form-status', '').trim());
    var toTopBtn = document.getElementById('toTop');
    if (toTopBtn) toTopBtn.setAttribute('aria-label', tr('back_to_top'));
    document.dispatchEvent(new Event('langchange'));
  };
  qsa('.lang-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var next = this.dataset.setLang === 'id' ? 'id' : 'en';
      document.documentElement.lang = next;
      try { localStorage.setItem('lang', next); } catch (e) {}
      syncLang();
    });
  });
  syncLang();

  // ---- Back to top button (appears after scrolling down) ----
  var toTop = document.getElementById('toTop');
  if (toTop) {
    var onScroll = function () { toTop.hidden = window.scrollY < 700; };
    window.addEventListener('scroll', onScroll, { passive: true });
    toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
    onScroll();
  }

  // ---- Scroll fade-in ----
  var fadeEls = qsa('.fade-in');
  if (fadeEls.length && 'IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function (entries) {
      var n = 0;
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var el = entry.target;
          if (n) { el.style.transitionDelay = Math.min(n, 5) * 90 + 'ms'; setTimeout(function () { el.style.transitionDelay = ''; }, 1100); }   // cards that appear together enter one after another
          n++;
          el.classList.add('visible'); obs.unobserve(el);
        }
      });
    }, { threshold: 0, rootMargin: '0px 0px -60px 0px' });
    fadeEls.forEach(function (el) { obs.observe(el); });
  } else {
    fadeEls.forEach(function (el) { el.classList.add('visible'); });
  }
});
