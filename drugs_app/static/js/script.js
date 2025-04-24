// Funkcja animująca liczniki
function animateCounters() {
  const counters = document.querySelectorAll(".counter");

  counters.forEach((counter) => {
    const target = parseInt(counter.getAttribute("data-target"));
    const duration = 1500; // ms
    const step = target / (duration / 16); // 60fps

    let current = 0;
    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        counter.textContent = target;
        clearInterval(timer);
      } else {
        counter.textContent = Math.round(current);
      }
    }, 16);
  });
}

// Obsługa formularza predykcji
document.addEventListener("DOMContentLoaded", function () {
  // Animacja przy scrollowaniu
  const animatedElements = document.querySelectorAll(".animate-fade");

  if (animatedElements.length > 0) {
    // Animuj elementy widoczne od razu
    animatedElements.forEach((el) => {
      if (isElementInViewport(el)) {
        el.style.opacity = "1";
        el.style.transform = "translateY(0)";
      }
    });

    // Dodaj listener na scroll
    window.addEventListener("scroll", function () {
      animatedElements.forEach((el) => {
        if (isElementInViewport(el) && el.style.opacity !== "1") {
          el.style.opacity = "1";
          el.style.transform = "translateY(0)";
        }
      });
    });
  }

  // Obsługa przycisku generowania profili
  const generateButton = document.getElementById("generateProfiles");
  if (generateButton) {
    generateButton.addEventListener("click", function () {
      // Symulacja ładowania
      this.innerHTML =
        '<i class="fas fa-spinner fa-spin me-2"></i>Generowanie...';
      this.disabled = true;

      // Symulacja opóźnienia
      setTimeout(() => {
        // Aktualizacja tabeli z profilami
        const tbody = document.querySelector("table tbody");
        if (tbody) {
          tbody.innerHTML = `
                      <tr>
                          <td>18-24</td>
                          <td>K</td>
                          <td>1.67</td>
                          <td>1.93</td>
                          <td>90%</td>
                      </tr>
                      <tr>
                          <td>25-34</td>
                          <td>M</td>
                          <td>1.12</td>
                          <td>0.84</td>
                          <td>72%</td>
                      </tr>
                      <tr>
                          <td>18-24</td>
                          <td>M</td>
                          <td>2.34</td>
                          <td>1.25</td>
                          <td>88%</td>
                      </tr>
                  `;
        }

        // Aktualizacja wykresu
        const newData = {
          x: [1.67, 1.12, 2.34, -0.28, 0.93, 1.56],
          y: [1.93, 0.84, 1.25, -0.42, 0.51, 0.97],
          marker: {
            color: [0.9, 0.72, 0.88, 0.18, 0.54, 0.65],
            colorscale: "Viridis",
            size: 14,
          },
        };

        Plotly.restyle("profilesChart", newData, 0);

        // Przywrócenie przycisku
        this.innerHTML =
          '<i class="fas fa-sync-alt me-2"></i>Wygeneruj nowe profile';
        this.disabled = false;
      }, 1500);
    });
  }

  // Obsługa przycisku aktualizacji wykresu
  const updateButton = document.getElementById("updateChart");
  if (updateButton) {
    updateButton.addEventListener("click", function () {
      // Symulacja ładowania
      this.innerHTML =
        '<i class="fas fa-spinner fa-spin me-2"></i>Aktualizowanie...';
      this.disabled = true;

      // Symulacja opóźnienia
      setTimeout(() => {
        // Losowa aktualizacja wykresu
        const chartTypes = document.getElementById("chartType").value;
        const drugTypes = document.getElementById("drugType").value;

        // Tutaj byłaby prawdziwa aktualizacja wykresu bazująca na API
        // Teraz symuluję ją losowymi zmianami
        const newData = [
          {
            x: ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
            y: [
              Math.floor(Math.random() * 300) + 100,
              Math.floor(Math.random() * 250) + 100,
              Math.floor(Math.random() * 200) + 100,
              Math.floor(Math.random() * 150) + 100,
              Math.floor(Math.random() * 100) + 50,
              Math.floor(Math.random() * 50) + 20,
            ],
            type: "bar",
            name: "Użytkownicy",
            marker: {
              color: "rgba(187, 134, 252, 0.8)",
            },
          },
          {
            x: ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
            y: [
              Math.floor(Math.random() * 150) + 50,
              Math.floor(Math.random() * 200) + 100,
              Math.floor(Math.random() * 250) + 150,
              Math.floor(Math.random() * 300) + 200,
              Math.floor(Math.random() * 350) + 250,
              Math.floor(Math.random() * 400) + 300,
            ],
            type: "bar",
            name: "Nie-użytkownicy",
            marker: {
              color: "rgba(3, 218, 198, 0.8)",
            },
          },
        ];

        Plotly.newPlot("chart", newData, {
          title: `Rozkład używania ${
            drugTypes === "all"
              ? "wszystkich narkotyków"
              : drugTypes === "opioid"
              ? "opioidów"
              : drugTypes === "ecstasy"
              ? "ekstazy"
              : "benzodiazepin"
          } według ${
            chartTypes === "age"
              ? "wieku"
              : chartTypes === "gender"
              ? "płci"
              : chartTypes === "education"
              ? "edukacji"
              : "zdrowia psychicznego"
          }`,
          barmode: "group",
          paper_bgcolor: "rgba(0,0,0,0)",
          plot_bgcolor: "rgba(0,0,0,0)",
          font: {
            color: "#e0e0e0",
          },
        });

        // Przywrócenie przycisku
        this.innerHTML =
          '<i class="fas fa-sync-alt me-2"></i>Aktualizuj wykres';
        this.disabled = false;
      }, 1000);
    });
  }
});

// Sprawdzenie czy element jest widoczny w oknie przeglądarki
function isElementInViewport(el) {
  const rect = el.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <=
      (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}
