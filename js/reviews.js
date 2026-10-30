/* Reviews carousel for v5 */

(function () {
    const track    = document.getElementById('reviews-track');
    const dotsWrap = document.getElementById('rev-dots');
    const btnPrev  = document.getElementById('rev-prev');
    const btnNext  = document.getElementById('rev-next');
    if (!track) return;

    const cards = Array.from(track.querySelectorAll('.review-card'));
    const perPage = window.innerWidth < 900 ? 1 : 3;
    let current = 0;
    const total = Math.ceil(cards.length / perPage);

    // Build dots
    for (let i = 0; i < total; i++) {
        const dot = document.createElement('div');
        dot.className = 'rev-dot' + (i === 0 ? ' active' : '');
        dot.addEventListener('click', () => goTo(i));
        dotsWrap.appendChild(dot);
    }

    function goTo(page) {
        current = (page + total) % total;
        const offset = current * perPage;
        cards.forEach((card, i) => {
            card.style.display = (i >= offset && i < offset + perPage) ? 'flex' : 'none';
            card.classList.toggle('active-review', i === offset);
        });
        document.querySelectorAll('.rev-dot').forEach((d, i) => {
            d.classList.toggle('active', i === current);
        });
    }

    goTo(0);
    btnPrev.addEventListener('click', () => goTo(current - 1));
    btnNext.addEventListener('click', () => goTo(current + 1));

    // Update perPage on resize
    window.addEventListener('resize', () => {
        const newPer = window.innerWidth < 768 ? 1 : 3;
        if (newPer !== perPage) goTo(0);
    });
})();
