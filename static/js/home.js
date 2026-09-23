// Анимации главной: texts reveal в hero, барабаны-счётчики, 3D-наклон карточек.
(function () {
    var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

    // ---------- Texts reveal ----------
    document.querySelectorAll('.t-stagger').forEach(function (block) {
        void block.offsetHeight;
        requestAnimationFrame(function () { block.classList.add('is-shown'); });
    });

    // ---------- Spinning counter: <span class="t-reel" data-reel="87"></span> ----------
    var SPINS = 2;
    var cssVar = function (el, name) { return getComputedStyle(el).getPropertyValue(name).trim(); };

    function buildReel(el) {
        var value = String(el.dataset.reel);
        el.setAttribute('aria-label', value);
        el.textContent = '';
        var cols = [];
        value.split('').forEach(function (ch, i) {
            var col = document.createElement('span');
            col.className = 't-reel-col';
            col.setAttribute('aria-hidden', 'true');
            if (!/\d/.test(ch)) {
                col.innerHTML = '<span class="t-reel-digit">' + ch + '</span>';
                el.appendChild(col);
                return;
            }
            var strip = document.createElement('span');
            strip.className = 't-reel-strip';
            // Несколько полных оборотов 0–9, затем целевая цифра
            var html = '';
            for (var s = 0; s <= SPINS; s++) {
                for (var d = 0; d < 10; d++) html += '<span class="t-reel-digit">' + d + '</span>';
            }
            strip.innerHTML = html;
            col.appendChild(strip);
            el.appendChild(col);
            cols.push({strip: strip, digit: Number(ch), index: i});
        });
        return cols;
    }

    function spin(el) {
        var cols = buildReel(el);
        if (reduce) {
            cols.forEach(function (c) {
                c.strip.style.transform = 'translateY(calc(var(--reel-cell) * -' + (SPINS * 10 + c.digit) + '))';
            });
            return;
        }
        var dur = parseFloat(cssVar(el, '--reel-dur')) || 1400;
        var stagger = parseFloat(cssVar(el, '--reel-stagger')) || 90;
        var blur = parseFloat(cssVar(el, '--reel-spin-blur')) || 3;
        cols.forEach(function (c, i) {
            // Вертикальное размытие через SVG: CSS blur() смазал бы цифры вбок
            var id = 'reel-blur-' + Math.random().toString(36).slice(2);
            var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svg.setAttribute('width', '0');
            svg.setAttribute('height', '0');
            svg.style.position = 'absolute';
            svg.innerHTML = '<filter id="' + id + '"><feGaussianBlur stdDeviation="0 ' + blur + '"/></filter>';
            el.appendChild(svg);
            var gauss = svg.querySelector('feGaussianBlur');
            var delay = i * stagger;

            c.strip.style.filter = 'url(#' + id + ')';
            c.strip.style.transition = 'transform ' + dur + 'ms ' + cssVar(el, '--reel-ease') + ' ' + delay + 'ms';
            void c.strip.offsetHeight;
            c.strip.style.transform = 'translateY(calc(var(--reel-cell) * -' + (SPINS * 10 + c.digit) + '))';

            var start = performance.now() + delay;
            (function decay(now) {
                var t = Math.min(1, Math.max(0, (now - start) / (dur * 0.8)));
                gauss.setAttribute('stdDeviation', '0 ' + (blur * (1 - t)).toFixed(2));
                if (t < 1) requestAnimationFrame(decay);
                else { c.strip.style.filter = ''; svg.remove(); }
            })(performance.now());
        });
    }

    var reels = document.querySelectorAll('[data-reel]');
    if ('IntersectionObserver' in window) {
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                io.unobserve(entry.target);
                spin(entry.target);
            });
        }, {threshold: 0.6});
        reels.forEach(function (el) { io.observe(el); });
    } else {
        reels.forEach(spin);
    }

    // ---------- Avatar group hover + подпись с именем ----------
    document.querySelectorAll('.t-avatar-group').forEach(function (root) {
        var avatars = Array.prototype.slice.call(root.querySelectorAll('.t-avatar'));
        var caption = document.getElementById(root.dataset.avatarCaption);
        var nameEl = caption && caption.querySelector('[data-caption-name]');
        var roleEl = caption && caption.querySelector('[data-caption-role]');
        var defaultName = nameEl ? nameEl.textContent : '';
        var cs = getComputedStyle(document.documentElement);
        var num = function (name, fb) { var v = parseFloat(cs.getPropertyValue(name)); return isFinite(v) ? v : fb; };
        var ease = function (name, fb) { return cs.getPropertyValue(name).trim() || fb; };

        function setShifts(activeIdx, phase) {
            var lift = num('--avatar-lift', -10);
            var falloff = num('--avatar-falloff', 0.45);
            var scale = num('--avatar-scale', 1.12);
            var tf = phase === 'out'
                ? ease('--avatar-ease-out', 'cubic-bezier(0.34, 3.85, 0.64, 1)')
                : ease('--avatar-ease-in', 'cubic-bezier(0.22, 1, 0.36, 1)');
            avatars.forEach(function (el, i) {
                // Кривую выставляем до смены переменных: вверх — плавно, обратно — с пружиной
                el.style.transitionTimingFunction = tf;
                if (activeIdx == null) {
                    el.style.setProperty('--shift', '0px');
                    el.style.setProperty('--scale-active', '1');
                    return;
                }
                var d = Math.abs(i - activeIdx);
                el.style.setProperty('--shift', (lift * Math.pow(falloff, d)).toFixed(3) + 'px');
                el.style.setProperty('--scale-active', i === activeIdx ? String(scale) : '1');
            });
        }

        function showCaption(el) {
            if (!nameEl) return;
            nameEl.textContent = el ? el.dataset.name : defaultName;
            roleEl.textContent = el ? el.dataset.role : '';
        }

        avatars.forEach(function (el, i) {
            el.addEventListener('mouseenter', function () { if (!reduce) setShifts(i, 'in'); showCaption(el); });
            el.addEventListener('focus', function () { showCaption(el); });
        });
        root.addEventListener('mouseleave', function () { if (!reduce) setShifts(null, 'out'); showCaption(null); });
    });

    // ---------- Card hover tilt (только мышь: на тач-экранах не мешаем прокрутке) ----------
    if (reduce || !matchMedia('(hover: hover) and (pointer: fine)').matches) return;

    document.querySelectorAll('.t-tilt').forEach(function (tilt) {
        var card = tilt.querySelector('.t-tilt-card');
        var max = Number(tilt.dataset.tiltMax || 10);

        function reset() {
            tilt.classList.remove('is-hover');
            card.classList.remove('is-tilting');
            card.style.setProperty('--tilt-rx', '0deg');
            card.style.setProperty('--tilt-ry', '0deg');
        }

        tilt.addEventListener('pointermove', function (e) {
            var r = tilt.getBoundingClientRect();
            var px = Math.min(1, Math.max(0, (e.clientX - r.left) / r.width));
            var py = Math.min(1, Math.max(0, (e.clientY - r.top) / r.height));
            tilt.classList.add('is-hover');
            card.classList.add('is-tilting');
            card.style.setProperty('--tilt-ry', ((px - 0.5) * max).toFixed(2) + 'deg');
            card.style.setProperty('--tilt-rx', ((0.5 - py) * max).toFixed(2) + 'deg');
            card.style.setProperty('--tilt-gx', (px * 100).toFixed(1) + '%');
            card.style.setProperty('--tilt-gy', (py * 100).toFixed(1) + '%');
        });
        tilt.addEventListener('pointerleave', reset);
    });
})();
