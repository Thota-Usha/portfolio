// ==========================================================================
// PORTFOLIO INTERACTIVITY & VERCEL INTEGRATION — SCRIPT.JS
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
  // 1. Initialize Lucide Icons
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // 2. Set Dynamic Footer Year
  const yearSpan = document.getElementById("year");
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }

  // API base URL for local development (if backend is running)
  const isLocalHost =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1";
  const API_BASE = isLocalHost && window.location.port === "8000" ? "" : "http://127.0.0.1:8000";

  // ==========================================================================
  // 3. Mobile Navigation Menu Toggle
  // ==========================================================================
  const mobileMenuBtn = document.getElementById("mobile-menu-btn");
  const navLinks = document.getElementById("nav-links");

  if (mobileMenuBtn && navLinks) {
    mobileMenuBtn.addEventListener("click", () => {
      navLinks.classList.toggle("open");
    });

    navLinks.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        navLinks.classList.remove("open");
      });
    });
  }

  // ==========================================================================
  // 4. Active Navigation Link on Scroll
  // ==========================================================================
  const sections = document.querySelectorAll("section[id]");
  const navItems = document.querySelectorAll(".nav-links a");

  window.addEventListener("scroll", () => {
    let currentSection = "";
    const scrollY = window.scrollY;

    sections.forEach((section) => {
      const sectionTop = section.offsetTop - 120;
      const sectionHeight = section.offsetHeight;
      if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
        currentSection = section.getAttribute("id");
      }
    });

    navItems.forEach((item) => {
      item.classList.remove("active");
      if (item.getAttribute("href") === `#${currentSection}`) {
        item.classList.add("active");
      }
    });
  });

  // ==========================================================================
  // 5. Visitor Counter (Local Backend or Simulated Persistent Storage)
  // ==========================================================================
  const visitorCountEl = document.getElementById("visitor-count");
  if (visitorCountEl) {
    if (isLocalHost) {
      fetch(`${API_BASE}/api/visit`, { method: "POST" })
        .then((res) => res.json())
        .then((data) => {
          if (data && data.total_views) visitorCountEl.textContent = data.total_views;
        })
        .catch(() => {
          handleClientVisitorCount();
        });
    } else {
      handleClientVisitorCount();
    }
  }

  function handleClientVisitorCount() {
    let views = parseInt(localStorage.getItem("usha_portfolio_views") || "142", 10);
    views += 1;
    localStorage.setItem("usha_portfolio_views", views);
    if (visitorCountEl) visitorCountEl.textContent = views;
  }

  // ==========================================================================
  // 6. Contact Form (Direct Email to thotaushasree09@gmail.com on Vercel)
  // ==========================================================================
  const contactForm = document.getElementById("contact-form");
  const formStatus = document.getElementById("form-status");

  if (contactForm) {
    contactForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const name = document.getElementById("name").value.trim();
      const email = document.getElementById("email").value.trim();
      const message = document.getElementById("message").value.trim();
      const submitBtn = contactForm.querySelector("button[type='submit']");

      if (submitBtn) submitBtn.disabled = true;
      if (formStatus) formStatus.textContent = "Delivering message to Usha Sree...";

      // Try local backend if running locally
      if (isLocalHost) {
        try {
          const response = await fetch(`${API_BASE}/api/contact`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, message }),
          });

          if (response.ok) {
            showSuccess(name);
            return;
          }
        } catch (err) {
          console.log("Local backend not running, falling back to direct email delivery.");
        }
      }

      // Live / Vercel Delivery: Direct Email to Usha via Web3Forms
      try {
        const formData = new FormData(contactForm);
        const res = await fetch("https://api.web3forms.com/submit", {
          method: "POST",
          body: formData,
        });

        const data = await res.json();
        if (data.success) {
          showSuccess(name);
          return;
        } else {
          throw new Error(data.message || "Delivery failed");
        }
      } catch (err) {
        // Ultimate Reliable Fallback: Open default email client with pre-filled fields
        const subject = encodeURIComponent(`Software Engineering / Job Opportunity from ${name}`);
        const body = encodeURIComponent(
          `Name: ${name}\nEmail: ${email}\n\nMessage:\n${message}`
        );
        window.location.href = `mailto:thotaushasree09@gmail.com?subject=${subject}&body=${body}`;

        if (formStatus) {
          formStatus.innerHTML = `📬 <strong>Opening your email app...</strong> You can hit send to reach Usha directly!`;
          formStatus.style.color = "#2563eb";
        }
      } finally {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  }

  function showSuccess(name) {
    if (formStatus) {
      formStatus.innerHTML = `✅ <strong>Message Delivered!</strong> Thank you ${name}, your inquiry has been sent directly to Usha's inbox.`;
      formStatus.style.color = "#047857";
    }
    contactForm.reset();
  }

  // ==========================================================================
  // 7. Floating AI Resume Assistant Chatbot (Works both Online & Offline)
  // ==========================================================================
  const chatToggleBtn = document.getElementById("chat-toggle-btn");
  const chatWindow = document.getElementById("chat-window");
  const chatCloseBtn = document.getElementById("chat-close-btn");
  const chatForm = document.getElementById("chat-input-form");
  const chatInput = document.getElementById("chat-input");
  const chatMessages = document.getElementById("chat-messages");
  const chipButtons = document.querySelectorAll(".chip-btn");

  if (chatToggleBtn && chatWindow) {
    chatToggleBtn.addEventListener("click", () => {
      chatWindow.classList.toggle("open");
      if (chatWindow.classList.contains("open")) {
        if (chatInput) chatInput.focus();
        scrollChatToBottom();
      }
    });
  }

  if (chatCloseBtn && chatWindow) {
    chatCloseBtn.addEventListener("click", () => {
      chatWindow.classList.remove("open");
    });
  }

  // Quick suggestion chips
  chipButtons.forEach((chip) => {
    chip.addEventListener("click", () => {
      const query = chip.getAttribute("data-query");
      if (query) {
        sendChatMessage(query);
      }
    });
  });

  // Handle Form Submission
  if (chatForm && chatInput) {
    chatForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const message = chatInput.value.trim();
      if (message) {
        sendChatMessage(message);
        chatInput.value = "";
      }
    });
  }

  function scrollChatToBottom() {
    if (chatMessages) {
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  }

  function appendChatMessage(sender, text) {
    if (!chatMessages) return;
    const msgDiv = document.createElement("div");
    msgDiv.className = `chat-msg ${sender}`;

    let formattedText = text
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      .replace(/\n/g, "<br>");

    msgDiv.innerHTML = formattedText;
    chatMessages.appendChild(msgDiv);
    scrollChatToBottom();
  }

  async function sendChatMessage(query) {
    appendChatMessage("user", query);

    const typingDiv = document.createElement("div");
    typingDiv.className = "chat-msg bot";
    typingDiv.id = "chat-typing";
    typingDiv.innerHTML = "<em>Analyzing resume...</em>";
    chatMessages.appendChild(typingDiv);
    scrollChatToBottom();

    // Try backend if local
    if (isLocalHost) {
      try {
        const response = await fetch(`${API_BASE}/api/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: query }),
        });

        if (response.ok) {
          const data = await response.json();
          removeTyping();
          appendChatMessage("bot", data.reply);
          return;
        }
      } catch (err) {
        // Fall back to client knowledge engine
      }
    }

    // Client-side AI Resume Knowledge Engine (Guarantees 100% uptime on Vercel)
    setTimeout(() => {
      removeTyping();
      const reply = answerFromClientKnowledge(query);
      appendChatMessage("bot", reply);
    }, 450);
  }

  function removeTyping() {
    const typingEl = document.getElementById("chat-typing");
    if (typingEl) typingEl.remove();
  }

  function answerFromClientKnowledge(query) {
    const q = query.toLowerCase();

    // 1. Greetings
    if (/\b(hi|hello|hey|greetings|namaste)\b/.test(q)) {
      return (
        "Hello! I am Usha Sree's AI Portfolio Assistant. 👋\n\n" +
        "Usha is a B.Tech CSE student at KL University (8.7 CGPA) actively seeking Full-Time Software Engineering (SDE) and Developer roles.\n" +
        "Ask me about her **Skills**, **Projects**, **Education**, or **Contact details**!"
      );
    }

    // 2. Education & CGPA
    if (/college|university|cgpa|marks|education|degree|branch|btech|b\.tech|year/.test(q)) {
      return (
        "🎓 **Education Details:**\n" +
        "• **Degree:** B.Tech in Computer Science & Engineering (CSE)\n" +
        "• **Institution:** KL University (Koneru Lakshmaiah Education Foundation), Vijayawada, AP\n" +
        "• **Current Year:** 3rd Year (Aug 2024 – May 2028)\n" +
        "• **Current CGPA:** **8.7 / 10.0**\n" +
        "• **Coursework:** Data Structures & Algorithms, OOPs, DBMS, Full-Stack Web Development."
      );
    }

    // 3. Skills
    if (/skill|stack|tech|languages|python|java|tools|c language/.test(q)) {
      return (
        "💻 **Technical Skills & Stack:**\n" +
        "• **Languages:** Python, C, Java, JavaScript (ES6+), SQL\n" +
        "• **Web Technologies:** HTML5, CSS3, Tailwind CSS, FastAPI, REST APIs, JWT Auth\n" +
        "• **Databases & Tools:** PostgreSQL (Supabase), MySQL, SQLite, Git & GitHub, PySpark, Pandas, Postman, VS Code\n" +
        "• **Core CS:** DSA, Object-Oriented Programming, Database Design, Agile Methodology."
      );
    }

    // 4. Projects
    if (/project|work|portfolio|placement|restaurant|bistro|spark/.test(q)) {
      return (
        "🚀 **Featured Projects by Usha Sree:**\n\n" +
        "1. **Campus Placement & Recruitment Drive Portal**\n" +
        "   • *Stack:* Python, FastAPI, Supabase PostgreSQL, Tailwind CSS, JWT Auth\n" +
        "   • *Live Demo:* https://placement-tracker-production-2c01.up.railway.app\n\n" +
        "2. **Savory AI Bistro (Full-Stack Restaurant App)**\n" +
        "   • *Stack:* Python, SQLite, JavaScript, Gemini AI, JWT Auth\n" +
        "   • *Features:* 22+ regional Telugu dishes, persistent cart, allergen collision safety shield.\n\n" +
        "3. **Food Delivery Big Data Analytics & Café App**\n" +
        "   • *Stack:* PySpark, Python, Pandas, MySQL, HTML/CSS/JS\n" +
        "   • *Features:* Big data pipeline analyzing delivery metrics + full café management UI."
      );
    }

    // 5. Why Hire / Job Roles
    if (/hire|why|job|career|full-time|fulltime|sde|engineer|intern|role|position/.test(q)) {
      return (
        "🌟 **Why Hire Usha Sree as a Software Engineer?**\n\n" +
        "• **Strong Academic & Practical Foundation:** Maintains an **8.7 CGPA** in CSE at KL University while building real-world software.\n" +
        "• **Full-Stack Competence:** Proficient in Python (FastAPI), modern frontend UI (Tailwind CSS, HTML/JS), and Cloud Databases (Supabase PostgreSQL, MySQL).\n" +
        "• **Proven Deliverables:** Deployed production web platforms (Campus Placement Tracker on Railway Cloud, Savory AI Bistro, Big Data PySpark pipeline).\n" +
        "• **Immediate Availability:** Open to campus recruitment, Full-Time Software Engineer (SDE) roles, and engineering opportunities."
      );
    }

    // 6. Contact & Socials
    if (/contact|email|reach|hire|phone|linkedin|github|location/.test(q)) {
      return (
        "📬 **Get in Touch with Usha Sree:**\n" +
        "• **Email:** thotaushasree09@gmail.com\n" +
        "• **LinkedIn:** https://www.linkedin.com/in/usha-sree-thota-a27a94366/\n" +
        "• **GitHub:** https://github.com/Thota-Usha\n" +
        "• **Location:** Vijayawada / Guntur, Andhra Pradesh, India"
      );
    }

    // Default
    return (
      "Thank you for asking! Usha Sree Thota is a 3rd-year B.Tech CSE student at KL University (8.7 CGPA) with expertise in Python, C, SQL, and Full-Stack Web Development.\n\n" +
      "Would you like to know more about her **Skills**, **Projects**, or **Contact details**?"
    );
  }
});
