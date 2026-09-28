// Año en footer
document.getElementById('year').textContent = new Date().getFullYear();

// Menú móvil
const nav = document.getElementById('main-nav');
const toggle = document.querySelector('.nav-toggle');
toggle.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
});

// Scroll suave para anclas internas
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const id = a.getAttribute('href');
    if (id.length > 1) {
      e.preventDefault();
      document.querySelector(id)?.scrollIntoView({behavior:'smooth', block:'start'});
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
});

// Nota: el inicio de sesión ahora es un enlace directo a la pantalla de
// login real de Django/allauth (ver index.html), ya no hay modal falso.

// Validación simple de formularios
document.getElementById('applyForm').addEventListener('submit', (e) => {
  e.preventDefault();
  const form = e.currentTarget;
  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }
  // Aquí podrías integrar tu backend (fetch/POST)
  alert('¡Gracias por tu interés! Hemos recibido tu solicitud.');
  form.reset();
});

// Galería: lightbox
// Lightbox (a prueba de fallos)
const lb = document.getElementById('lightbox');
const lbImg = document.getElementById('lightboxImg');
const lbClose = document.querySelector('.lightbox-close');

// Asegura oculto al iniciar (por si algún CSS lo rompe)
if (lb) lb.hidden = true;

// Abre al hacer click en miniaturas (si existen)
document.querySelectorAll('.gallery .g-item').forEach(link => {
  link.addEventListener('click', (e) => {
    if (!lb || !lbImg) return;
    e.preventDefault();
    lbImg.removeAttribute('src');      // limpia fuente anterior
    lbImg.alt = link.querySelector('img')?.alt || 'Imagen ampliada';
    lbImg.src = link.getAttribute('href');
    lb.hidden = false;
  });
});

// Cerrar con botón ×
if (lbClose && lb) {
  lbClose.addEventListener('click', () => { lb.hidden = true; });
}

// Cerrar al hacer click fuera de la imagen
if (lb) {
  lb.addEventListener('click', (e) => {
    if (e.target === lb) lb.hidden = true;
  });
}

// Cerrar con tecla ESC
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && lb && !lb.hidden) lb.hidden = true;
});


// Animación on-scroll (reveal)
const reveal = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting){
      entry.target.style.transform = 'translateY(0)';
      entry.target.style.opacity = '1';
      reveal.unobserve(entry.target);
    }
  });
}, {threshold: 0.15});

document.querySelectorAll('.card, .gallery .g-item, .pill').forEach(el => {
  el.style.transform = 'translateY(12px)';
  el.style.opacity = '.001';
  el.style.transition = 'all .6s ease';
  reveal.observe(el);
});
let lastY = window.scrollY;
function compactHeader(){
  const y = window.scrollY;
  const compact = y > 24;
  document.body.classList.toggle('header-compact', compact);
  setHeaderH();
  lastY = y;
}
window.addEventListener('scroll', compactHeader, { passive: true });
compactHeader();
