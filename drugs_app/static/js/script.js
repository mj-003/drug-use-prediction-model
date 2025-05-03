// Function to animate counters
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

// Event handlers when the document is loaded
document.addEventListener("DOMContentLoaded", function () {
  // Animate elements on scroll
  const animatedElements = document.querySelectorAll(".animate-fade");

  if (animatedElements.length > 0) {
    // Animate elements visible immediately
    animatedElements.forEach((el) => {
      if (isElementInViewport(el)) {
        el.style.opacity = "1";
        el.style.transform = "translateY(0)";
      }
    });

    // Add scroll listener
    window.addEventListener("scroll", function () {
      animatedElements.forEach((el) => {
        if (isElementInViewport(el) && el.style.opacity !== "1") {
          el.style.opacity = "1";
          el.style.transform = "translateY(0)";
        }
      });
    });
  }

  // Initialize any interactive components
  initializeFormValidation();
});

// Initialize form validation
function initializeFormValidation() {
  const predictionForm = document.querySelector('form[action*="predict"]');

  if (predictionForm) {
    // Add custom validation for numeric fields
    const numericInputs = predictionForm.querySelectorAll(
      'input[type="number"]'
    );

    numericInputs.forEach((input) => {
      input.addEventListener("input", function () {
        const value = parseFloat(this.value);
        const min = parseFloat(this.getAttribute("min"));
        const max = parseFloat(this.getAttribute("max"));

        if (value < min) {
          this.setCustomValidity(`Value should be at least ${min}`);
        } else if (value > max) {
          this.setCustomValidity(`Value should be at most ${max}`);
        } else {
          this.setCustomValidity("");
        }
      });
    });

    // Add submission handler
    predictionForm.addEventListener("submit", function (e) {
      // Check if form is valid
      if (!this.checkValidity()) {
        e.preventDefault();
        e.stopPropagation();

        // Highlight invalid fields
        const invalidInputs = this.querySelectorAll(":invalid");
        invalidInputs.forEach((input) => {
          input.classList.add("is-invalid");

          // Add an error message
          const formGroup = input.closest(".col-md-4");
          if (formGroup) {
            let errorMessage = input.validationMessage;
            let errorDiv = formGroup.querySelector(".invalid-feedback");

            if (!errorDiv) {
              errorDiv = document.createElement("div");
              errorDiv.className = "invalid-feedback";
              input.after(errorDiv);
            }

            errorDiv.textContent = errorMessage;
          }
        });
      }

      // Add loading state to submit button
      const submitBtn = this.querySelector('button[type="submit"]');
      if (submitBtn) {
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML =
          '<i class="fas fa-spinner fa-spin me-2"></i>Przetwarzanie...';
        submitBtn.disabled = true;

        // Set a timeout to restore the button if the form doesn't submit
        setTimeout(() => {
          if (submitBtn.disabled) {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
          }
        }, 5000);
      }
    });

    // Reset invalid state when input changes
    predictionForm.addEventListener("input", function (e) {
      if (e.target.classList.contains("is-invalid")) {
        e.target.classList.remove("is-invalid");

        // Remove error message
        const formGroup = e.target.closest(".col-md-4");
        if (formGroup) {
          const errorDiv = formGroup.querySelector(".invalid-feedback");
          if (errorDiv) {
            errorDiv.textContent = "";
          }
        }
      }
    });
  }

  // Improve number input interaction
  const allNumericInputs = document.querySelectorAll('input[type="number"]');
  allNumericInputs.forEach((input) => {
    // Add step buttons for accessibility
    input.addEventListener("wheel", function (e) {
      e.preventDefault();

      // Only proceed if input is focused
      if (document.activeElement === this) {
        const step = parseFloat(this.getAttribute("step") || 1);
        const currentVal = parseFloat(this.value) || 0;

        if (e.deltaY < 0) {
          // Scroll up - increase value
          this.value = currentVal + step;
        } else {
          // Scroll down - decrease value
          this.value = currentVal - step;
        }

        // Trigger input event
        this.dispatchEvent(new Event("input"));
      }
    });
  });
}

// Check if element is visible in the viewport
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
