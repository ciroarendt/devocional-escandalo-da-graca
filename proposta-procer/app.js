// ===== REVEAL ON SCROLL =====
document.addEventListener('DOMContentLoaded', function () {

  // Add reveal class to animatable elements
  var targets = document.querySelectorAll(
    '.card, .timeline-item, .audience-item, .diff-item, ' +
    '.pricing-card, .path-card, .step, .cta-box, ' +
    '.section-title, .section-desc, .stats-row, ' +
    '.curiosity-card, .meeting-cta, .auth-box, .pricing-wrapper'
  );

  targets.forEach(function (el) {
    el.classList.add('reveal');
  });

  // Intersection Observer
  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  );

  document.querySelectorAll('.reveal').forEach(function (el) {
    observer.observe(el);
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Enter key in auth input
  var authInput = document.getElementById('authInput');
  if (authInput) {
    authInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        checkPassword();
      }
    });
  }
});

// ===== AUTHENTICATION =====
function checkPassword() {
  var input = document.getElementById('authInput');
  var btn = document.getElementById('authBtn');
  var error = document.getElementById('authError');
  var authBox = document.getElementById('authBox');
  var pricingWrapper = document.getElementById('pricingWrapper');

  if (!input || !pricingWrapper || !authBox) return;

  var value = input.value.trim().toLowerCase();

  // Accepted passwords (case-insensitive)
  var validCodes = ['procer2026', 'epic', 'agil', 'agile', 'liderança'];

  if (validCodes.indexOf(value) !== -1) {
    // Success — hide auth box, show pricing
    btn.classList.add('loading');
    btn.textContent = 'Verificando...';

    setTimeout(function () {
      authBox.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      authBox.style.opacity = '0';
      authBox.style.transform = 'translateY(-10px)';

      setTimeout(function () {
        authBox.style.display = 'none';
        pricingWrapper.style.display = 'block';
        pricingWrapper.style.animation = 'unlock 0.6s ease forwards';
        pricingWrapper.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 400);
    }, 600);

  } else {
    // Wrong password — shake + show error
    error.style.display = 'block';
    input.style.borderColor = '#e05c5c';
    input.value = '';
    input.focus();

    // Reset border after a moment
    setTimeout(function () {
      input.style.borderColor = '';
    }, 2000);
  }
}
