/* Anwar Alumni Network JavaScript Utilities */

document.addEventListener('DOMContentLoaded', function() {
    // 1. Counter animation for statistics
    const counters = document.querySelectorAll('.counter-value');
    const speed = 200;

    const animateCounters = () => {
        counters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText;
            const inc = Math.max(1, Math.ceil(target / speed));

            if (count < target) {
                counter.innerText = count + inc;
                setTimeout(animateCounters, 15);
            } else {
                counter.innerText = target;
            }
        });
    };

    // Trigger counter animation when stats section enters viewport
    const statsElem = document.querySelector('.stats-section');
    if (statsElem) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounters();
                    observer.disconnect();
                }
            });
        }, { threshold: 0.2 });
        observer.observe(statsElem);
    }

    // 2. Copy Bank Account Number to Clipboard
    const copyBtns = document.querySelectorAll('.copy-btn');
    copyBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetId = this.getAttribute('data-copy-target');
            const targetElem = document.getElementById(targetId);
            if (targetElem) {
                const textToCopy = targetElem.innerText.trim();
                navigator.clipboard.writeText(textToCopy).then(() => {
                    const originalText = this.innerHTML;
                    this.innerHTML = '<i class="bi bi-check-lg"></i> Copied!';
                    this.classList.add('btn-success');
                    setTimeout(() => {
                        this.innerHTML = originalText;
                        this.classList.remove('btn-success');
                    }, 2000);
                });
            }
        });
    });

    // 3. Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#' && targetId.length > 1) {
                const targetElem = document.querySelector(targetId);
                if (targetElem) {
                    e.preventDefault();
                    targetElem.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
});
