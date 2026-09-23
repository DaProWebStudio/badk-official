(function () {
    // ---------- Шапка ----------
    var header = document.getElementById('site-header');
    var nav = document.getElementById('site-nav');
    var burger = document.getElementById('site-burger');
    var toTop = document.getElementById('to-top');

    function onScroll() {
        var y = window.scrollY;
        if (header) header.classList.toggle('is-scrolled', y > 40);
        if (toTop) toTop.classList.toggle('is-visible', y > 600);
    }
    window.addEventListener('scroll', onScroll, {passive: true});
    onScroll();

    if (toTop) {
        toTop.addEventListener('click', function () {
            window.scrollTo({top: 0, behavior: 'smooth'});
        });
    }

    if (nav && burger) {
        var setMenu = function (open) {
            nav.classList.toggle('is-open', open);
            burger.classList.toggle('is-open', open);
            burger.setAttribute('aria-expanded', String(open));
            document.documentElement.classList.toggle('overflow-hidden', open);
        };

        burger.addEventListener('click', function () {
            setMenu(!nav.classList.contains('is-open'));
        });

        var items = nav.querySelectorAll('[data-dropdown]');
        var closeAll = function (except) {
            items.forEach(function (item) {
                if (item === except) return;
                item.classList.remove('is-open');
                item.querySelector('button').setAttribute('aria-expanded', 'false');
            });
        };

        items.forEach(function (item) {
            var btn = item.querySelector('button');
            btn.addEventListener('click', function () {
                var open = !item.classList.contains('is-open');
                closeAll(item);
                item.classList.toggle('is-open', open);
                btn.setAttribute('aria-expanded', String(open));
            });
        });

        document.addEventListener('click', function (e) {
            if (!e.target.closest('[data-dropdown]') && window.innerWidth >= 1280) closeAll();
        });

        document.addEventListener('keydown', function (e) {
            if (e.key !== 'Escape') return;
            closeAll();
            if (nav.classList.contains('is-open')) setMenu(false);
        });

        window.addEventListener('resize', function () {
            if (window.innerWidth >= 1280 && nav.classList.contains('is-open')) setMenu(false);
        });
    }

    // ---------- Ленты со стрелками: <div data-rail-for="id">[prev][next]</div> ----------
    document.querySelectorAll('[data-rail-for]').forEach(function (group) {
        var rail = document.getElementById(group.dataset.railFor);
        if (!rail) return;
        var prev = group.querySelector('[data-dir="-1"]');
        var next = group.querySelector('[data-dir="1"]');
        function sync() {
            prev.disabled = rail.scrollLeft <= 4;
            next.disabled = rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 4;
        }
        [prev, next].forEach(function (btn) {
            btn.addEventListener('click', function () {
                rail.scrollBy({left: Number(btn.dataset.dir) * rail.clientWidth * 0.8, behavior: 'smooth'});
            });
        });
        rail.addEventListener('scroll', sync, {passive: true});
        window.addEventListener('resize', sync);
        sync();
    });

    // ---------- Появление при прокрутке: атрибут data-reveal ----------
    var targets = document.querySelectorAll('[data-reveal]');
    if (targets.length && 'IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
        targets.forEach(function (el) {
            // Соседние карточки появляются по очереди
            var i = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
            el.style.setProperty('--i', Math.min(i, 5));
        });
        document.documentElement.classList.add('reveal-on');
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                var el = entry.target;
                el.classList.add('is-in');
                io.unobserve(el);
                // После появления возвращаем элементу его собственные transition и hover
                var delay = 800 + 70 * (Number(el.style.getPropertyValue('--i')) || 0);
                setTimeout(function () {
                    el.removeAttribute('data-reveal');
                    el.classList.remove('is-in');
                }, delay);
            });
        }, {rootMargin: '0px 0px -8% 0px', threshold: 0.08});
        targets.forEach(function (el) { io.observe(el); });
    }
})();
