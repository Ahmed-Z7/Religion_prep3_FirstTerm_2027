// Islamic Education Booklet Interactive Scripts

document.addEventListener('DOMContentLoaded', () => {
  // Theme Toggle
  const themeBtn = document.getElementById('themeToggle');
  const currentTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', currentTheme);
  updateThemeIcon(currentTheme);

  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const activeTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = activeTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      updateThemeIcon(newTheme);
    });
  }

  function updateThemeIcon(theme) {
    if (!themeBtn) return;
    themeBtn.innerHTML = theme === 'dark' ? '☀️ الوضع الفاتح' : '🌙 الوضع الليلي';
  }

  // Print Action
  const printBtn = document.getElementById('printBtn');
  if (printBtn) {
    printBtn.addEventListener('click', () => {
      window.print();
    });
  }

  // Font Size Adjuster
  let fontSize = 16;
  const zoomInBtn = document.getElementById('zoomIn');
  const zoomOutBtn = document.getElementById('zoomOut');

  if (zoomInBtn) {
    zoomInBtn.addEventListener('click', () => {
      if (fontSize < 22) {
        fontSize += 1;
        document.body.style.fontSize = fontSize + 'px';
      }
    });
  }

  if (zoomOutBtn) {
    zoomOutBtn.addEventListener('click', () => {
      if (fontSize > 13) {
        fontSize -= 1;
        document.body.style.fontSize = fontSize + 'px';
      }
    });
  }

  // Toggle All Answers
  const toggleAnswersBtn = document.getElementById('toggleAnswersBtn');
  let answersVisible = true;
  if (toggleAnswersBtn) {
    toggleAnswersBtn.addEventListener('click', () => {
      answersVisible = !answersVisible;
      const answers = document.querySelectorAll('.answer-reveal, .q-answer');
      answers.forEach(el => {
        el.style.display = answersVisible ? 'flex' : 'none';
      });
      toggleAnswersBtn.textContent = answersVisible ? '👁️ إخفاء الإجابات للاختبار الذاتي' : '👁️ إظهار جميع الإجابات';
    });
  }

  // Search Filter
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const query = e.target.value.trim().toLowerCase();
      const cards = document.querySelectorAll('.lesson-card, .qa-card');
      
      cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        if (text.includes(query)) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    });
  }

  // Interactive Quiz Clicks for MCQ Options
  const optionButtons = document.querySelectorAll('.option-btn');
  optionButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      const parent = this.closest('.qa-card');
      if (!parent) return;
      const isCorrect = this.getAttribute('data-correct') === 'true';
      const siblings = parent.querySelectorAll('.option-btn');
      
      siblings.forEach(s => {
        s.style.borderColor = '';
        s.style.backgroundColor = '';
        if (s.getAttribute('data-correct') === 'true') {
          s.classList.add('correct');
        }
      });

      if (!isCorrect) {
        this.style.backgroundColor = '#fee2e2';
        this.style.borderColor = '#ef4444';
        this.style.color = '#b91c1c';
      }

      const reveal = parent.querySelector('.answer-reveal');
      if (reveal) {
        reveal.style.display = 'flex';
      }
    });
  });
});
