//Alterando tema claro escuro
document.addEventListener("DOMContentLoaded", () => {
  // Theme Toggle Logic
  const toggleBtn = document.getElementById("theme-toggle");
  const iconElement = toggleBtn?.querySelector("i"); // Use um nome diferente para o elemento do ícone

  if (toggleBtn && iconElement) {
    function setTheme(theme) {
      document.documentElement.setAttribute("data-theme", theme);
      localStorage.setItem("theme", theme);
      iconElement.className = theme === "dark" ? "fa-solid fa-sun" : "fa-solid fa-moon";
    }

    toggleBtn.addEventListener("click", () => {
      const currentTheme = document.documentElement.getAttribute("data-theme");
      setTheme(currentTheme === "dark" ? "light" : "dark");
    });

    // Inicialização do tema
    const savedTheme = localStorage.getItem("theme") || "dark"; // Padrão para dark
    setTheme(savedTheme);
  } else {
    console.warn("Theme toggle button or its icon element not found.");
  }

  // Smooth Scroll & Highlight Logic
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href')?.substring(1);

      if (targetId) {
        const targetElement = document.getElementById(targetId); // Nome diferente para o elemento alvo
        if (targetElement) {
          // Calcula o offset do header se ele for fixo/sticky
          const header = document.querySelector("header");
          const headerOffset = header ? header.offsetHeight : 0;
          const elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
          const offsetPosition = elementPosition - headerOffset - 20; // 20px de margem extra

          window.scrollTo({
            top: offsetPosition,
            behavior: "smooth"
          });

          // Efeito de destaque
          targetElement.classList.add('highlight');
          setTimeout(() => {
            if (targetElement) { // Verifica se o elemento ainda existe
                targetElement.classList.remove('highlight');
            }
          }, 1000);
        } else {
          console.warn(`Target element with ID '${targetId}' not found for scroll.`);
        }
      }
    });
  });

  // GSAP Animations navegação na página
  if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);

    gsap.utils.toArray("main section > article, main section > div.day-container, main section > div.organizers-container").forEach(element => {
      gsap.from(element, {
        opacity: 0,
        y: 50,
        duration: 0.8, // Duração um pouco menor para parecer mais rápido
        ease: "power2.out",
        scrollTrigger: {
          trigger: element,
          start: "top 85%", // Inicia um pouco mais tarde na tela
          end: "bottom 20%",
          toggleActions: "play none none none", // play na entrada, nada ao sair
          // markers: true, // Descomente para debugar o ScrollTrigger
        }
      });
    });

    // Animação específica para o título do banner se desejar
    if (document.querySelector('.banner-title')) {
        gsap.from(".banner-title", { opacity: 0, y: -30, duration: 1, delay: 0.3 });
    }
    if (document.querySelector('.banner-subtitle')) {
        gsap.from(".banner-subtitle", { opacity: 0, y: -30, duration: 1, delay: 0.5 });
    }
     if (document.querySelector('.banner-location')) {
        gsap.from(".banner-location", { opacity: 0, y: -30, duration: 1, delay: 0.7 });
    }
     if (document.querySelector('#datas-importantes')) {
        gsap.from("#datas-importantes .date-card", {
            opacity: 0,
            y: 30,
            duration: 0.5,
            stagger: 0.2, // Anima os cards em sequência
            scrollTrigger: {
                trigger: "#datas-importantes",
                start: "top 80%"
            }
        });
    }


  } else {
    console.warn("GSAP or ScrollTrigger not loaded. Animations will not run.");
  }
});


document.addEventListener('DOMContentLoaded', () => {
  const menuMobile = document.querySelector('.menu-mobile');
  const links = menuMobile.querySelectorAll('a');

  links.forEach(link => {
    link.addEventListener('click', () => {
      menuMobile.removeAttribute('open');
    });
  });
});


// Máscara de telefone
document.getElementById('telefone').addEventListener('input', function (e) {
  let input = e.target.value.replace(/\D/g, '');
  if (input.length > 11) input = input.slice(0, 11);
  let formatted = '';
  if (input.length > 0) {
    formatted += '(' + input.substring(0, 2);
  }
  if (input.length >= 3) {
    formatted += ') ' + input.substring(2, 7);
  }
  if (input.length >= 8) {
    formatted += '-' + input.substring(7, 11);
  }
  e.target.value = formatted;
});

//Mensagem flash temporária
window.addEventListener("DOMContentLoaded", () => {
  const flashMessages = document.querySelectorAll(".flash-message");
  setTimeout(() => {
    flashMessages.forEach(msg => {
      msg.classList.add("flash-hidden");
    });
  }, 5000); // 5 segundos
});

//fade out mensagem flash
document.addEventListener('DOMContentLoaded', function () {
  const flashMessages = document.querySelectorAll('.flash-message');
  flashMessages.forEach(msg => {
    setTimeout(() => {
      msg.style.opacity = '0';
      setTimeout(() => {
        msg.remove();  // Remove do DOM após desaparecer
      }, 1000); // Tempo para completar a transição
    }, 5000); // Espera 5 segundos antes de começar a desaparecer
  });
});


//envia mensagem e exibe o flash sem carregar
document.getElementById("contato-form").addEventListener("submit", async function(event) {
  event.preventDefault(); // impede envio tradicional

  const form = event.target;
  const formData = new FormData(form);

  const response = await fetch("/enviar_mensagem", {
    method: "POST",
    body: formData
  });

  const result = await response.json();
  mostrarMensagem(result.mensagem, result.categoria);
  form.reset(); // limpa o formulário, se desejar
});

function mostrarMensagem(texto, categoria) {
  const container = document.getElementById("flash-container");
  container.innerHTML = `<div class="flash-message flash-${categoria}">${texto}</div>`;
  
  setTimeout(() => {
    container.innerHTML = "";
  }, 5000);
}


//Carroussel Banners
let slideIndex = 0;
let slides = document.querySelectorAll('.carousel-slide');
let autoSlide = true;

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.remove('active');
  });

  slides[index].classList.add('active');
}

function mudarSlide(n) {
  slideIndex += n;
  if (slideIndex >= slides.length) slideIndex = 0;
  if (slideIndex < 0) slideIndex = slides.length - 1;
  showSlide(slideIndex);
}

function iniciarAutoSlide() {
  setInterval(() => {
    if (autoSlide) {
      mudarSlide(1);
    }
  }, 3000);
}

document.addEventListener('DOMContentLoaded', () => {
  showSlide(slideIndex);
  iniciarAutoSlide();
});