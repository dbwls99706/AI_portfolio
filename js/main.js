/* ============================================
   YuJin Hong Portfolio — JavaScript
   ============================================ */

(function () {
  'use strict';

  // --- Typing Animation ---
  const roles = [
    'Full-Stack Developer',
    'AI Application Developer',
    'Robotics Software Engineer',
    'Open-Source Contributor',
  ];

  const heroRoleText = document.getElementById('heroRoleText');
  let roleIndex = 0;
  let charIndex = 0;
  let isDeleting = false;

  function typeRole() {
    const current = roles[roleIndex];

    if (isDeleting) {
      heroRoleText.textContent = current.substring(0, charIndex - 1);
      charIndex--;
    } else {
      heroRoleText.textContent = current.substring(0, charIndex + 1);
      charIndex++;
    }

    let delay = isDeleting ? 40 : 80;

    if (!isDeleting && charIndex === current.length) {
      delay = 2000;
      isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      roleIndex = (roleIndex + 1) % roles.length;
      delay = 400;
    }

    setTimeout(typeRole, delay);
  }

  if (heroRoleText) {
    setTimeout(typeRole, 600);
  }

  // --- Navigation Scroll Effect ---
  const nav = document.getElementById('nav');

  function handleNavScroll() {
    if (window.scrollY > 50) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
  }

  window.addEventListener('scroll', handleNavScroll, { passive: true });

  // --- Mobile Menu Toggle ---
  const navToggle = document.getElementById('navToggle');
  const mobileMenu = document.getElementById('mobileMenu');

  if (navToggle && mobileMenu) {
    navToggle.addEventListener('click', function () {
      mobileMenu.classList.toggle('open');
    });

    mobileMenu.querySelectorAll('.mobile-link').forEach(function (link) {
      link.addEventListener('click', function () {
        mobileMenu.classList.remove('open');
      });
    });
  }

  // --- Active Nav Link Tracking ---
  const sections = document.querySelectorAll('.section, .hero');
  const navLinks = document.querySelectorAll('.nav-link');

  function updateActiveNav() {
    let current = '';
    var scrollY = window.scrollY;

    sections.forEach(function (section) {
      var top = section.offsetTop - 100;
      if (scrollY >= top) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(function (link) {
      link.classList.remove('active');
      if (link.getAttribute('data-section') === current) {
        link.classList.add('active');
      }
    });
  }

  window.addEventListener('scroll', updateActiveNav, { passive: true });

  // --- Scroll Animations (Intersection Observer) ---
  var fadeElements = document.querySelectorAll('.fade-in');

  if ('IntersectionObserver' in window) {
    var fadeObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            fadeObserver.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: '0px 0px -40px 0px',
      }
    );

    fadeElements.forEach(function (el) {
      fadeObserver.observe(el);
    });
  } else {
    // Fallback: show all elements
    fadeElements.forEach(function (el) {
      el.classList.add('visible');
    });
  }

  // --- GitHub API: Fetch Live Star Counts ---
  var GITHUB_USERNAME = 'dbwls99706';
  var REPOS_TO_TRACK = [
    'max-level-ant',
    'OpenSource-contribution-card',
    'Velog_Backup',
    'yolov8_on_raspberrypi4',
    'Robotics_Control',
  ];

  function fetchGitHubStats() {
    var apiUrl =
      'https://api.github.com/users/' +
      GITHUB_USERNAME +
      '/repos?per_page=100&sort=updated';

    fetch(apiUrl)
      .then(function (response) {
        if (!response.ok) throw new Error('GitHub API error');
        return response.json();
      })
      .then(function (repos) {
        var totalStars = 0;
        var projectCount = 0;

        repos.forEach(function (repo) {
          if (!repo.fork) {
            totalStars += repo.stargazers_count;

            if (REPOS_TO_TRACK.indexOf(repo.name) !== -1) {
              projectCount++;
              updateRepoStars(repo.name, repo.stargazers_count);
            }
          }
        });

        // Update global stats
        var statStars = document.getElementById('statStars');
        if (statStars && totalStars > 0) {
          statStars.textContent = totalStars;
        }

        var statRepos = document.getElementById('statRepos');
        if (statRepos) {
          var nonForkCount = repos.filter(function (r) {
            return !r.fork;
          }).length;
          statRepos.textContent = nonForkCount;
        }
      })
      .catch(function () {
        // Silent fail — static fallback values already in HTML
      });
  }

  function updateRepoStars(repoName, stars) {
    // Update star badges
    var badges = document.querySelectorAll(
      '[data-repo-stars="' + repoName + '"]'
    );
    badges.forEach(function (badge) {
      if (stars > 0) {
        badge.textContent = stars + (stars === 1 ? ' star' : ' stars');
      }
    });

    // Update highlight values
    var highlights = document.querySelectorAll(
      '[data-live-stars="' + repoName + '"]'
    );
    highlights.forEach(function (el) {
      if (stars > 0) {
        el.textContent = stars;
      }
    });
  }

  // Fetch stats on load
  fetchGitHubStats();

  // --- Smooth Scroll for Anchor Links ---
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var href = this.getAttribute('href');
      if (href === '#') return;

      var target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        var offset = 80;
        var top =
          target.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }
    });
  });
})();
