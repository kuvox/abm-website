(function () {
  var IMG = {
    compressorNew: '../images/subaru-compressor-new.png',
    compressorUsed: '../images/subaru-compressor-used.png',
    compressor2002: '../images/subaru-compressor-2002.png',
    apparel: '../images/shopping-tile-apparel.svg',
    industrial: '../images/shopping-tile-industrial.svg'
  };

  var SCENARIOS = {
    automotive: {
      inputPlaceholder: 'e.g. dkv10r compressor',
      feed: {
        product_type: 'automotive > replacement parts > subaru > impreza > DKV10R',
        title: 'A/C Compressor - 2015-2019 Subaru WRX STI 2.5L H4',
        mpn: '129872-03724743',
        condition: 'new',
        question_and_answer: 'Question: Does it fit my 2014 Subaru Impreza? Answer: No, it only fits 2015 to 2019 models.'
      },
      queries: {
        'dkv10r-compressor': {
          text: 'dkv10r compressor',
          fields: ['product_type', 'title'],
          note: 'DKV10R in <em>product_type</em> and &ldquo;compressor&rdquo; in the <em>title</em>.'
        },
        'dkv10r-subaru-ac': {
          text: 'used dkv10r subaru ac',
          fields: ['product_type', 'title'],
          note: 'DKV10R and Subaru in <em>product_type</em>; &ldquo;used&rdquo; steers the match toward the resale listing.'
        },
        'subaru-air-compressor': {
          text: 'subaru air compressor',
          fields: ['product_type', 'title'],
          note: 'Subaru in <em>product_type</em> and compressor/air language in the <em>title</em>.'
        },
        'mpn-exact': {
          text: '129872-03724743',
          fields: ['mpn'],
          note: 'Exact match on the manufacturer part number (<em>mpn</em>).'
        },
        'clutch-impreza': {
          text: 'compressor with clutch 2014 impreza',
          fields: ['product_type', 'title', 'question_and_answer'],
          note: '&ldquo;Compressor&rdquo; in the <em>title</em>, Impreza in <em>product_type</em>, and the 2014 fit question in <em>question_and_answer</em>.'
        },
        'dkv10r-wrx-fit': {
          text: 'does a DKV10R compressor fit subaru 2002 wrx',
          fields: ['product_type', 'title', 'question_and_answer'],
          note: 'DKV10R and Subaru in the feed; the <em>question_and_answer</em> field can power AI Overview fitment answers.',
          aiOverview: 'No, the DKV10R compressor will not fit a 2002 Subaru WRX. The DKV10R (often associated with Zexel/Valeo) is primarily designed for later-generation Subaru models (typically 2007\u20132014 Impreza, WRX, and Forester models equipped with 2.5L engines).'
        }
      },
      tiles: [
        {
          id: 'compressor-new',
          image: IMG.compressorNew,
          title: 'A/C Compressor - 2015-2019 Subaru WRX STI 2.5L H4',
          subtitle: 'WRX STI 2.5L H4',
          price: '$168.95',
          brand: 'Premium Autoparts',
          mpn: '129872-03724743',
          productType: 'automotive > replacement parts > subaru > wrx sti > DKV10R'
        },
        {
          id: 'compressor-used',
          image: IMG.compressorUsed,
          used: true,
          previewSearch: 'used subaru air conditioning compressor',
          title: 'Used Compressor - 2015 Subaru WRX STI',
          subtitle: '2015 WRX STI',
          price: '$75.00',
          brand: 'Autoparts Resale',
          productType: 'automotive > replacement parts > subaru > wrx sti > used'
        },
        {
          id: 'compressor-2002',
          image: IMG.compressor2002,
          previewSearch: 'does a DKV10R compressor fit subaru 2002 wrx',
          title: '2002 Subaru WRX A/C Compressor',
          subtitle: '2002 WRX',
          price: '$122.50',
          brand: 'Classic Parts',
          arrivesBy: 'Arrives by 5/25',
          productType: 'automotive > replacement parts > subaru > wrx > 2002'
        }
      ]
    },
    apparel: {
      inputPlaceholder: "e.g. nike pegasus size 11",
      feed: {
        product_type: 'apparel > shoes > running > nike > pegasus',
        title: 'Nike Air Zoom Pegasus 40 - Men\'s Running Shoe',
        mpn: 'DV3853-001',
        condition: 'new',
        availability: 'in-stock',
        question_and_answer: 'Question: Does this run true to size? Answer: Yes, most runners order their usual Nike size.'
      },
      queries: {
        'nike-pegasus': {
          text: 'nike pegasus size 11',
          fields: ['product_type', 'title'],
          note: 'Nike and Pegasus in <em>product_type</em> and <em>title</em>; size is a common shopper modifier.'
        },
        'mens-running': {
          text: "men's running shoes",
          fields: ['product_type', 'title'],
          note: 'Running category in <em>product_type</em> and &ldquo;Men&rsquo;s Running Shoe&rdquo; in the <em>title</em>.'
        },
        'yoga-leggings': {
          text: 'black yoga leggings',
          fields: [],
          note: 'This search matches the leggings Shopping ad on the right &mdash; not the featured running shoe in the center feed.'
        },
        'waterproof-jacket': {
          text: 'waterproof jacket',
          fields: [],
          note: 'This search would surface a jacket SKU when that <em>product_type</em> exists in your feed &mdash; neither sample ad qualifies here.'
        }
      },
      tiles: [
        {
          id: 'pegasus',
          image: IMG.apparel,
          title: "Nike Air Zoom Pegasus 40",
          subtitle: "Men's - Size 11",
          price: '$129.99',
          brand: 'Nike',
          productType: 'apparel > shoes > running > nike > pegasus'
        },
        {
          id: 'leggings',
          image: IMG.apparel,
          title: 'High-Rise Yoga Leggings',
          subtitle: 'Black - Large',
          price: '$48.00',
          brand: 'Lululemon',
          productType: 'apparel > activewear > leggings > yoga'
        }
      ]
    },
    industrial: {
      inputPlaceholder: 'e.g. 3/4 ball valve brass',
      feed: {
        product_type: 'industrial > valves > ball valves > brass > 3/4 inch',
        title: '3/4" Brass Ball Valve - Full Port - 600 WOG',
        mpn: 'BV-075-BR-600',
        condition: 'new',
        availability: 'in-stock',
        question_and_answer: 'Question: Is this lead-free brass? Answer: Yes, meets NSF/ANSI 61 for potable water.'
      },
      queries: {
        'ball-valve': {
          text: '3/4 ball valve brass',
          fields: ['product_type', 'title'],
          note: 'Ball valve and brass in <em>product_type</em>; 3/4&Prime; sizing in the <em>title</em>.'
        },
        'pipe-fitting': {
          text: 'stainless pipe fitting',
          fields: [],
          note: 'Pipe fittings share industrial vocabulary but use a different <em>product_type</em> path than the featured ball valve.'
        },
        'hydraulic-hose': {
          text: 'hydraulic hose 24 inch',
          fields: [],
          note: 'This search would match a hose SKU in your catalog &mdash; neither sample ad qualifies here.'
        },
        'work-gloves': {
          text: 'nitrile work gloves',
          fields: [],
          note: 'PPE searches map to safety categories &mdash; see the gloves ad brighten on the right.'
        }
      },
      tiles: [
        {
          id: 'ball-valve',
          image: IMG.industrial,
          title: '3/4" Brass Ball Valve',
          subtitle: 'Full Port - 600 WOG',
          price: '$42.50',
          brand: 'Smith Valve Co.',
          productType: 'industrial > valves > ball valves > brass > 3/4 inch'
        },
        {
          id: 'gloves',
          image: IMG.industrial,
          title: 'Nitrile Work Gloves',
          subtitle: 'Large - 12 Pack',
          price: '$29.99',
          brand: 'Mechanix',
          productType: 'industrial > safety > gloves > nitrile'
        }
      ]
    }
  };

  var TOKEN_ALIASES = {
    ac: ['a/c', 'air conditioning', 'air'],
    conditioning: ['a/c', 'air conditioning'],
    air: ['a/c', 'compressor']
  };

  var FIELD_ORDER = [
    'product_type', 'title', 'mpn', 'condition', 'availability', 'question_and_answer'
  ];

  function normalize(text) {
    return (text || '').trim().toLowerCase().replace(/\s+/g, ' ');
  }

  function normalizeField(text) {
    return normalize(text).replace(/\//g, '');
  }

  function tokenize(text) {
    return normalize(text).split(' ').filter(function (t) {
      return t.length > 1 || /^\d+$/.test(t);
    });
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function tokenMatchesField(token, fieldName, fieldText) {
    var haystack = normalizeField(fieldText);
    var needle = normalizeField(token);

    if (haystack.indexOf(needle) !== -1) return true;

    var aliases = TOKEN_ALIASES[needle];
    if (aliases) {
      for (var i = 0; i < aliases.length; i++) {
        if (haystack.indexOf(normalizeField(aliases[i])) !== -1) return true;
      }
    }

    if (needle === 'ac' && fieldName === 'title' && haystack.indexOf('a/c') !== -1) return true;
    if ((needle === 'air' || needle === 'conditioning') && fieldName === 'title') {
      return haystack.indexOf('a/c') !== -1 || haystack.indexOf('compressor') !== -1;
    }

    return false;
  }

  function tileMatchScore(tile, searchText) {
    var tokens = tokenize(searchText);
    if (!tokens.length) return 0;

    var productType = normalizeField(tile.productType);
    var title = normalizeField(tile.title);
    var price = normalizeField(tile.price || '');
    var subtitle = normalizeField(tile.subtitle || '');
    var mpn = normalizeField(tile.mpn || '');
    var queryNorm = normalize(searchText);
    var score = 0;

    tokens.forEach(function (token) {
      var needle = normalizeField(token);

      if (mpn && mpn.indexOf(needle) !== -1) score += 12;
      if (productType.indexOf(needle) !== -1) score += 3;
      if (title.indexOf(needle) !== -1) score += 3;
      if (subtitle.indexOf(needle) !== -1) score += 2;
      if (price.indexOf(needle) !== -1) score += 4;

      var aliases = TOKEN_ALIASES[token];
      if (aliases) {
        aliases.forEach(function (alias) {
          var a = normalizeField(alias);
          if (productType.indexOf(a) !== -1 || title.indexOf(a) !== -1) score += 2;
        });
      }
    });

    if (queryNorm.indexOf('used') !== -1) {
      if (title.indexOf('used') !== -1 || subtitle.indexOf('used') !== -1 || price.indexOf('used') !== -1) score += 6;
      else score -= 2;
    }

    if (queryNorm.indexOf('impreza') !== -1 && (title.indexOf('impreza') !== -1 || productType.indexOf('impreza') !== -1)) {
      score += 4;
    }

    if (queryNorm.indexOf('dkv10r') !== -1 && productType.indexOf('dkv10r') !== -1) score += 6;

    if (queryNorm.indexOf('2002') !== -1) {
      if (title.indexOf('2002') !== -1) score += 12;
      else if (title.indexOf('2015') !== -1 || title.indexOf('2019') !== -1) score -= 5;
    }

    return score;
  }

  function tileMatchesSearch(tile, searchText) {
    return tileMatchScore(tile, searchText) > 0;
  }

  function getWinningTileId(tiles, searchText) {
    if (!normalize(searchText)) return null;

    var scores = tiles.map(function (tile) {
      return { id: tile.id, score: tileMatchScore(tile, searchText) };
    });

    var maxScore = scores.reduce(function (best, item) {
      return item.score > best ? item.score : best;
    }, 0);

    if (maxScore <= 0) return null;

    var winner = scores.find(function (item) { return item.score === maxScore; });
    return winner ? winner.id : null;
  }

  function findFirstQualifyingQueryKey(scenario, tileId) {
    var keys = Object.keys(scenario.queries);
    for (var i = 0; i < keys.length; i++) {
      if (getWinningTileId(scenario.tiles, scenario.queries[keys[i]].text) === tileId) {
        return keys[i];
      }
    }
    return null;
  }

  function renderFeedPlaceholder(container) {
    container.innerHTML = '<p class="feed-data-placeholder" data-feed-placeholder>To preview relevant product data, click a keyword or shopping ad.</p>';
    container.classList.add('feed-fields--empty');
  }

  function renderFeedFields(container, feed) {
    container.classList.remove('feed-fields--empty');
    var html = FIELD_ORDER.filter(function (key) {
      return Object.prototype.hasOwnProperty.call(feed, key);
    }).map(function (key) {
      var value = feed[key] || '';
      var mismatchHint = key === 'condition'
        ? '<span class="feed-field-mismatch-hint" data-feed-mismatch-hint hidden>Search says used; feed says new</span>'
        : '';
      return (
        '<div class="feed-field" data-feed-field="' + key + '">' +
          '<span class="feed-field-label">' + key + '</span>' +
          '<span class="feed-field-value">' + escapeHtml(value) + '</span>' +
          mismatchHint +
        '</div>'
      );
    }).join('');
    container.innerHTML = html;
  }

  function renderQueries(container, scenario) {
    var html = Object.keys(scenario.queries).map(function (key) {
      var q = scenario.queries[key];
      return '<li><button type="button" data-feed-query="' + key + '">' + escapeHtml(q.text) + '</button></li>';
    }).join('');
    container.innerHTML = html;
  }

  function renderTileFooter(tile) {
    if (tile.used) {
      return '<p class="feed-shopping-tile-footer">Used</p>';
    }
    return '<p class="feed-shopping-tile-footer">' + escapeHtml(tile.arrivesBy || 'Arrives by 5/4') + '</p>';
  }

  function renderTiles(container, tiles) {
    var html = tiles.map(function (tile) {
      var subtitle = tile.subtitle
        ? '<p class="feed-shopping-tile-subtitle">' + escapeHtml(tile.subtitle) + '</p>'
        : '';
      var usedClass = tile.used ? ' feed-shopping-tile--used-product' : '';
      var mediaClass = /\.png$/i.test(tile.image) ? ' feed-shopping-tile-media--photo' : '';
      return (
        '<article class="feed-shopping-tile' + usedClass + '" data-feed-tile="' + tile.id + '" data-product-type="' + escapeHtml(tile.productType) + '" role="button" tabindex="0" aria-label="Preview keyword match for ' + escapeHtml(tile.title) + '">' +
          '<div class="feed-shopping-tile-media' + mediaClass + '">' +
            '<img src="' + tile.image + '" alt="" class="feed-shopping-tile-img" loading="lazy">' +
          '</div>' +
          '<div class="feed-shopping-tile-body">' +
            '<p class="feed-shopping-tile-title">' + escapeHtml(tile.title) + '</p>' +
            subtitle +
            '<p class="feed-shopping-tile-price">' + escapeHtml(tile.price) + '</p>' +
            '<p class="feed-shopping-tile-brand">' + escapeHtml(tile.brand) + '</p>' +
            renderTileFooter(tile) +
          '</div>' +
        '</article>'
      );
    }).join('');
    container.innerHTML = html;
  }

  function init(root) {
    var scenarioKey = 'automotive';
    var scenario = SCENARIOS[scenarioKey];
    var activeSearchText = '';

    var queryListEl = root.querySelector('[data-feed-query-list]');
    var fieldsEl = root.querySelector('[data-feed-fields]');
    var tilesEl = root.querySelector('[data-feed-shopping-tiles]');
    var aiOverviewEl = root.querySelector('[data-feed-ai-overview]');
    var aiOverviewTextEl = root.querySelector('[data-feed-ai-overview-text]');
    var inputEl = root.querySelector('[data-feed-search-input]');
    var tabEls = root.querySelectorAll('[data-feed-scenario]');
    var resetBtn = root.querySelector('[data-feed-reset]');

    function ensureFeedRendered() {
      if (!fieldsEl.querySelector('[data-feed-field]')) {
        renderFeedFields(fieldsEl, scenario.feed);
      }
    }

    function getFields() {
      return root.querySelectorAll('[data-feed-field]');
    }

    function getQueries() {
      return root.querySelectorAll('[data-feed-query]');
    }

    function getTiles() {
      return root.querySelectorAll('[data-feed-tile]');
    }

    function fieldValues() {
      var map = {};
      getFields().forEach(function (el) {
        var valueEl = el.querySelector('.feed-field-value');
        map[el.getAttribute('data-feed-field')] = valueEl ? valueEl.textContent : '';
      });
      return map;
    }

    function findQueryKey(text) {
      var normalized = normalize(text);
      if (!normalized) return null;
      var keys = Object.keys(scenario.queries);
      for (var i = 0; i < keys.length; i++) {
        if (normalize(scenario.queries[keys[i]].text) === normalized) return keys[i];
      }
      return null;
    }

    function resetFields() {
      getFields().forEach(function (el) {
        el.classList.remove('feed-field--matched', 'feed-field--dim', 'feed-field--mismatch');
        var hint = el.querySelector('[data-feed-mismatch-hint]');
        if (hint) hint.hidden = true;
      });
    }

    function resetQueries() {
      getQueries().forEach(function (el) { el.classList.remove('feed-query--active'); });
    }

    function resetAiOverview() {
      if (aiOverviewEl) aiOverviewEl.classList.remove('feed-ai-overview--active');
      if (aiOverviewTextEl) {
        aiOverviewTextEl.textContent = '';
        aiOverviewTextEl.hidden = true;
      }
    }

    function updateAiOverview(queryKey) {
      if (!aiOverviewEl || !aiOverviewTextEl) return;

      var query = queryKey ? scenario.queries[queryKey] : null;
      if (query && query.aiOverview) {
        aiOverviewEl.classList.add('feed-ai-overview--active');
        aiOverviewTextEl.textContent = query.aiOverview;
        aiOverviewTextEl.hidden = false;
        return;
      }

      resetAiOverview();
    }

    function resetTiles() {
      if (tilesEl) tilesEl.removeAttribute('data-winner');
      getTiles().forEach(function (el) {
        el.classList.remove('feed-shopping-tile--matched', 'feed-shopping-tile--dim');
      });
    }

    function applyTileHighlights(searchText) {
      resetTiles();
      var winnerId = getWinningTileId(scenario.tiles, searchText);
      if (!winnerId) return;

      if (tilesEl) tilesEl.setAttribute('data-winner', winnerId);

      getTiles().forEach(function (el) {
        if (el.getAttribute('data-feed-tile') === winnerId) {
          el.classList.add('feed-shopping-tile--matched');
        } else {
          el.classList.add('feed-shopping-tile--dim');
        }
      });
    }

    function clear(resetInput) {
      activeSearchText = '';
      resetQueries();
      resetTiles();
      resetAiOverview();
      renderFeedPlaceholder(fieldsEl);
      if (resetInput && inputEl) inputEl.value = '';
    }

    function applyState(match, searchText, options) {
      options = options || {};
      activeSearchText = searchText || '';
      ensureFeedRendered();
      resetFields();
      if (!options.keepQueries) resetQueries();

      if (options.key) {
        var btn = root.querySelector('[data-feed-query="' + options.key + '"]');
        if (btn) btn.classList.add('feed-query--active');
      }

      if (options.syncInput && inputEl && options.key) {
        inputEl.value = scenario.queries[options.key].text;
      }

      var matched = {};
      match.fields.forEach(function (name) { matched[name] = true; });

      var mismatched = {};
      (match.mismatch || []).forEach(function (name) { mismatched[name] = true; });

      var hasActive = match.fields.length || (match.mismatch || []).length || normalize(activeSearchText);

      getFields().forEach(function (el) {
        var name = el.getAttribute('data-feed-field');
        if (matched[name]) {
          el.classList.add('feed-field--matched');
        } else if (mismatched[name]) {
          el.classList.add('feed-field--mismatch');
          var hint = el.querySelector('[data-feed-mismatch-hint]');
          if (hint) hint.hidden = false;
        } else if (hasActive && match.fields.length) {
          el.classList.add('feed-field--dim');
        }
      });

      applyTileHighlights(activeSearchText);
      updateAiOverview(options.key || null);
    }

    function inferTokenMatch(text) {
      var values = fieldValues();
      var tokens = tokenize(text);
      if (!tokens.length) return null;

      var matched = {};
      var mismatch = {};
      var queryNorm = normalize(text);

      tokens.forEach(function (token) {
        Object.keys(values).forEach(function (fieldName) {
          if (tokenMatchesField(token, fieldName, values[fieldName])) {
            matched[fieldName] = true;
          }
        });

        if (token === 'used' && normalize(values.condition) === 'new') {
          mismatch.condition = true;
          delete matched.condition;
        }
      });

      if (queryNorm.indexOf('air conditioning') !== -1 && values.title) {
        matched.title = true;
      }

      var matchedNames = Object.keys(matched);
      if (!matchedNames.length && !Object.keys(mismatch).length) return null;

      return {
        fields: matchedNames,
        mismatch: Object.keys(mismatch),
        note: 'Best-effort match based on words in your search. Highlighted fields contain related terms from the feed.'
      };
    }

    function applyMatch(key, syncInput) {
      var match = scenario.queries[key];
      if (!match) return;
      applyState(match, match.text, { key: key, syncInput: syncInput });
    }

    function applyInput(text) {
      var key = findQueryKey(text);
      if (key) {
        applyMatch(key, false);
        return;
      }

      if (!normalize(text)) {
        clear(false);
        return;
      }

      var inferred = inferTokenMatch(text);
      if (inferred) {
        applyState(inferred, text, { keepQueries: true });
        return;
      }

      resetFields();
      resetQueries();
      resetTiles();
      resetAiOverview();
      activeSearchText = text;
    }

    function loadScenario(key) {
      if (!SCENARIOS[key]) return;
      scenarioKey = key;
      scenario = SCENARIOS[key];

      tabEls.forEach(function (tab) {
        var isActive = tab.getAttribute('data-feed-scenario') === key;
        tab.classList.toggle('feed-demo-tab--active', isActive);
        tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });

      if (inputEl) {
        inputEl.placeholder = scenario.inputPlaceholder;
        inputEl.id = 'feed-search-input-' + key;
        var label = root.querySelector('[data-feed-search-label]');
        if (label) label.setAttribute('for', inputEl.id);
      }

      renderQueries(queryListEl, scenario);
      renderTiles(tilesEl, scenario.tiles);
      clear(true);
    }

    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        clear(true);
      });
    }

    queryListEl.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-feed-query]');
      if (!btn) return;
      applyMatch(btn.getAttribute('data-feed-query'), true);
    });

    function previewTile(tileId) {
      var queryKey = findFirstQualifyingQueryKey(scenario, tileId);
      if (queryKey) {
        applyMatch(queryKey, true);
        return;
      }

      var tile = null;
      for (var i = 0; i < scenario.tiles.length; i++) {
        if (scenario.tiles[i].id === tileId) {
          tile = scenario.tiles[i];
          break;
        }
      }
      if (!tile || !tile.previewSearch) return;

      var inferred = inferTokenMatch(tile.previewSearch);
      if (inferred) {
        applyState(inferred, tile.previewSearch, { syncInput: true });
      }
    }

    tilesEl.addEventListener('click', function (e) {
      var tile = e.target.closest('[data-feed-tile]');
      if (!tile) return;
      previewTile(tile.getAttribute('data-feed-tile'));
    });

    tilesEl.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter' && e.key !== ' ') return;
      var tile = e.target.closest('[data-feed-tile]');
      if (!tile) return;
      e.preventDefault();
      previewTile(tile.getAttribute('data-feed-tile'));
    });

    tabEls.forEach(function (tab) {
      tab.addEventListener('click', function () {
        loadScenario(tab.getAttribute('data-feed-scenario'));
      });
    });

    if (inputEl) {
      inputEl.addEventListener('input', function () {
        applyInput(inputEl.value);
      });
      inputEl.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') applyInput(inputEl.value);
      });
    }

    loadScenario('automotive');
    initCursorHint(root.querySelector('[data-feed-demo-stage]'));
  }

  function initCursorHint(stage) {
    if (!stage) return;

    var wrap = stage.querySelector('[data-feed-cursor-hint]');
    var label = stage.querySelector('[data-feed-cursor-label]');
    var line = stage.querySelector('[data-feed-cursor-line]');
    if (!wrap || !label || !line) return;

    var mouse = { x: 0, y: 0 };
    var pos = { x: 0, y: 0 };
    var active = false;
    var rafId = 0;
    var offset = 14;

    function setPositions() {
      wrap.style.setProperty('--cursor-x', mouse.x + 'px');
      wrap.style.setProperty('--cursor-y', mouse.y + 'px');
      label.style.transform = 'translate(' + (pos.x + offset) + 'px, ' + (pos.y + offset) + 'px)';

      var dx = mouse.x - pos.x;
      var dy = mouse.y - pos.y;
      var dist = Math.sqrt(dx * dx + dy * dy);
      var angle = Math.atan2(dy, dx) * (180 / Math.PI);

      line.style.width = Math.max(dist, 1) + 'px';
      line.style.transform = 'translate(' + pos.x + 'px, ' + pos.y + 'px) rotate(' + angle + 'deg)';
    }

    function tick() {
      pos.x += (mouse.x - pos.x) * 0.14;
      pos.y += (mouse.y - pos.y) * 0.14;
      setPositions();
      if (active) rafId = requestAnimationFrame(tick);
    }

    stage.addEventListener('mouseenter', function (e) {
      var rect = stage.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
      pos.x = mouse.x;
      pos.y = mouse.y;
      wrap.hidden = false;
      active = true;
      setPositions();
      rafId = requestAnimationFrame(tick);
    });

    stage.addEventListener('mouseleave', function () {
      active = false;
      cancelAnimationFrame(rafId);
      wrap.hidden = true;
    });

    stage.addEventListener('mousemove', function (e) {
      var rect = stage.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
    });
  }

  document.querySelectorAll('[data-tool="feed-keyword-matcher"]').forEach(init);
})();
