// Countdown timer that updates days, hours, minutes, and seconds
function startCountdown(targetDateStr) {
  const daysEl = document.getElementById("countdown-days");
  const hoursEl = document.getElementById("countdown-hours");
  const minutesEl = document.getElementById("countdown-minutes");
  const secondsEl = document.getElementById("countdown-seconds");
  const targetDate = new Date(targetDateStr);
  function updateCountdown() {
    const now = new Date();
    let diff = Math.floor((targetDate - now) / 1000);
    if (diff < 0) diff = 0;
    const days = Math.floor(diff / (24 * 3600));
    const hours = Math.floor((diff % (24 * 3600)) / 3600);
    const minutes = Math.floor((diff % 3600) / 60);
    const seconds = diff % 60;
    daysEl.innerText = days;
    hoursEl.innerText = hours;
    minutesEl.innerText = minutes;
    secondsEl.innerText = seconds;
    if (diff === 0) {
      clearInterval(interval);
    }
  }
  updateCountdown();
  const interval = setInterval(updateCountdown, 1000);
}

// Automatically start countdown if featured event date is available
document.addEventListener("DOMContentLoaded", function () {
  // Get Started button
  var getStartedBtn = document.getElementById("get-started-btn");
  if (getStartedBtn) {
    getStartedBtn.addEventListener("click", function () {
      window.location.href = "/signup/";
    });
  }

  // Tickets & Details button
  var ticketsDetailsBtn = document.getElementById("tickets-details-btn");
  if (ticketsDetailsBtn) {
    ticketsDetailsBtn.addEventListener("click", function () {
      // Scroll to event details section
      document.getElementById("event-list").scrollIntoView({ behavior: "smooth" });
    });
  }

  // Join Now button
  var joinNowBtn = document.getElementById("join-now-btn");
  if (joinNowBtn) {
    joinNowBtn.addEventListener("click", function () {
      alert("Thank you for joining! See you at the event.");
    });
  }
  // You need to pass the featured event date from Django template to JS
  // For example, add a hidden input or data attribute in your template:
  // <div id="featured-event-date" data-date="{{ fast_event.date|date:'Y-m-d H:i:s' }}"></div>
  var featuredDateDiv = document.getElementById("featured-event-date");
  if (featuredDateDiv) {
    var dateStr = featuredDateDiv.getAttribute("data-date");
    if (dateStr) {
      startCountdown(dateStr);
    }
  }
});


// Event details modal logic
function showEventDetailsFromButton(btn) {
  const eventData = {
    id: btn.getAttribute("data-id"),
    name: btn.getAttribute("data-name"),
    description: btn.getAttribute("data-description"),
    category: { name: btn.getAttribute("data-category") },
    date: btn.getAttribute("data-date"),
    image: { url: btn.getAttribute("data-image") },
    location: btn.getAttribute("data-location"),
  };
  showEventDetails(eventData);
}

function showEventDetails(eventData) {
  const modal = document.getElementById("event-details");
  document.getElementById("event-img").src = eventData.image.url;
  document.getElementById("event-name").innerText = eventData.name;
  document.getElementById(
    "event-description"
  ).innerText = `Description: ${eventData.description}`;
  document.getElementById(
    "event-category"
  ).innerText = `Category: ${eventData.category.name}`;
  document.getElementById(
    "event-date-full"
  ).innerText = `Date: ${eventData.date}`;
  document.getElementById(
    "event-location"
  ).innerText = `Location: ${eventData.location}`;
  // Show modal with animation
  modal.classList.remove("hidden");
  setTimeout(() => {
    modal.classList.remove("opacity-0");
    modal.querySelector("div").classList.remove("scale-90");
    modal.querySelector("div").classList.add("scale-100");
    modal.classList.add("opacity-100");
  }, 10);
}

function closeEventDetails() {
  const modal = document.getElementById("event-details");
  modal.classList.remove("opacity-100");
  modal.classList.add("opacity-0");
  modal.querySelector("div").classList.remove("scale-100");
  modal.querySelector("div").classList.add("scale-90");
  setTimeout(() => {
    modal.classList.add("hidden");
  }, 300);
}


// Edit Event Page - Manage Participants
document.addEventListener('DOMContentLoaded', function () {
    const eventSelect = document.getElementById('event-participants');
    const selectedList = document.getElementById('selected-participants');
    const participantsContainer = document.getElementById('participant-inputs-container');

    // Function to create a hidden input for a participant
    function createHiddenInput(participantId) {
        // Check if the input already exists to prevent duplicates
        if (!participantsContainer.querySelector('input[value="' + participantId + '"]')) {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'participants'; // This name is crucial for the backend
            input.value = participantId;
            participantsContainer.appendChild(input);
        }
    }

    // Function to remove a hidden input
    function removeHiddenInput(participantId) {
        const input = participantsContainer.querySelector('input[value="' + participantId + '"]');
        if (input) {
            input.remove();
        }
    }

    // Function to add a participant to both the visual list and hidden inputs
    function addParticipantToList(participantId, participantName) {
        // Check if the participant is already in the visual list
        if (!selectedList.querySelector('li[data-value="' + participantId + '"]')) {
            const li = document.createElement('li');
            li.dataset.value = participantId;
            li.textContent = participantName;
            li.className = 'flex justify-between items-center bg-gray-100 p-2 my-1 rounded';

            const delBtn = document.createElement('button');
            delBtn.type = 'button';
            delBtn.textContent = 'Remove';
            delBtn.className = 'ml-2 text-red-500 hover:text-red-700 transition remove-li-btn';
            delBtn.addEventListener('click', function () {
                li.remove();
                removeHiddenInput(participantId);
                // Also, unselect from the dropdown
                const option = eventSelect.querySelector('option[value="' + participantId + '"]');
                if (option) option.selected = false;
            });

            li.appendChild(delBtn);
            selectedList.appendChild(li);
        }
    }

    // Step 1: Initialize hidden inputs for all existing participants
    document.querySelectorAll('.participant-row').forEach(row => {
        const participantId = row.dataset.value;
        createHiddenInput(participantId);
    });

    // Step 2: Handle adding new participants from the dropdown
    document.getElementById('add-participant').addEventListener('click', function () {
        Array.from(eventSelect.selectedOptions).forEach(option => {
            addParticipantToList(option.value, option.textContent);
            createHiddenInput(option.value);
            // Unselect from the dropdown after adding
            option.selected = false;
        });
    });

    // Step 3: Handle removing participants from the main table
    document.querySelectorAll('.remove-participant-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const row = btn.closest('tr');
            const participantId = row.dataset.value;
            row.remove(); // Remove the row from the table

            removeHiddenInput(participantId); // Remove the hidden input
            
            // Also, remove from the "Add Participants" visual list
            const liToRemove = selectedList.querySelector(`li[data-value="${participantId}"]`);
            if (liToRemove) liToRemove.remove();
        });
    });
});
