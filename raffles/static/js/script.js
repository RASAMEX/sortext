// DOM Elements
const slot1 = document.getElementById("slot1");
const slot2 = document.getElementById("slot2");
const slot3 = document.getElementById("slot3");
const button = document.getElementById("spin_button");
const button2 = document.getElementById("spin_button2");
const outputText = document.getElementById('output_text');
const terminal = document.getElementById('terminal');
const baseUrl = window.location.origin;

let names = [];
let ids = [];
let list = [];
let winner = null;

let counter1 = 0;
let counter2 = 0;
let counter3 = 0;
let lane1, lane2, lane3;
let intervalId1, intervalId2, intervalId3;
const speed = 100;

let invested = false;
let twoThree = false;
let level = 'soft';

const typeCheckbox = document.getElementById('elimination');
const typeCheckbox2 = document.getElementById('two_out_of_three');
const typeSelect = document.getElementById('level');

// Event Listeners
button.onclick = spin;
button2.onclick = repeat;

typeCheckbox.addEventListener('change', function () {
  invested = this.checked;
});

typeCheckbox2.addEventListener('change', function () {
  twoThree = this.checked;
});

typeSelect.addEventListener('change', function () {
  level = this.value;
});

/**
 * Updates the participants table via AJAX request.
 */
function updateTable() {
  $.ajax({
    url: updateParticipantsURL, 
    type: 'GET',
    success: function (data) {
      $('#participants-table').html(data);
    },
    error: function (error) {
      console.error('Error updating table:', error);
    }
  });
}

/**
 * Fetches data from a given URL.
 * @param {string} url - The URL to fetch data from.
 * @returns {Promise<Object|null>} The fetched data or null in case of an error.
 */
function fetchData(url) {
  return fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error('Request failed');
      }
      return response.json();
    })
    .then(data => data)
    .catch(error => {
      console.error('Error making request:', error);
      return null;
    });
}

/**
 * Spins a slot machine lane.
 * @param {HTMLElement} slot - The slot element to update.
 * @param {number} counter - The initial counter value.
 * @param {number} lane - The index of the lane to spin.
 * @returns {number} The interval ID for the spinning lane.
 */
function spinLane(slot, counter, lane) {
  return setInterval(() => {
    slot.textContent = names[counter];
    counter++;
    if (counter >= names.length) {
      counter = 0;
    }
  }, speed);
}

/**
 * Spins the slot machine once.
 */
function spin() {
  button.disabled = true;
  button2.disabled = true;

  const url = `${baseUrl}/draw/${raffle_id}/?invested=${invested}&two_three=${twoThree}&level=${level}`;
  fetchData(url)
    .then(result => {
      if (result) {
        let message = result.legend;
        if (result.result) {
          names = result.result.participating.map(participant => participant.name);
          ids = result.result.participating.map(participant => participant.id);
          list = result.list;
          lane1 = ids.indexOf(result.result.lane1);
          lane2 = ids.indexOf(result.result.lane2);
          lane3 = ids.indexOf(result.result.lane3);
          winner = result.result.winner;
        }
        outputText.innerHTML += `${message}<br>`;
        terminal.scrollTop = terminal.scrollHeight;
      } else {
        console.log('Failed to fetch data');
      }
    });

  setTimeout(() => {
    outputText.innerHTML += `Participating: ${names}<br>`;
    terminal.scrollTop = terminal.scrollHeight;
  }, 1000);

  setTimeout(() => {
    outputText.innerHTML += `Participant IDs: ${ids}<br>`;
    terminal.scrollTop = terminal.scrollHeight;
  }, 1500);

  setTimeout(() => {
    outputText.innerHTML += `Draw list: ${list}<br>`;
    terminal.scrollTop = terminal.scrollHeight;
  }, 2500);

  intervalId1 = spinLane(slot1, counter1, lane1);
  intervalId2 = spinLane(slot2, counter2, lane2);
  intervalId3 = spinLane(slot3, counter3, lane3);

  setTimeout(stopSpin, 3000);
  setTimeout(stopSpin2, 4000);
  setTimeout(stopSpin3, 5000);
}

/**
 * Stops the spinning of the first lane.
 */
function stopSpin() {
  clearInterval(intervalId1);
  slot1.textContent = names[lane1];
}

/**
 * Stops the spinning of the second lane.
 */
function stopSpin2() {
  clearInterval(intervalId2);
  slot2.textContent = names[lane2];
}

/**
 * Stops the spinning of the third lane.
 */
function stopSpin3() {
  clearInterval(intervalId3);
  slot3.textContent = names[lane3];

  updateTable();

  outputText.innerHTML += `Result: ${[lane1, lane2, lane3]} | Winner: ${winner ? winner : 'nobody'}<br>`;
  terminal.scrollTop = terminal.scrollHeight;
  checkConditions(winner, invested);
  button.disabled = false;
  button2.disabled = false;
}

/**
 * Repeats the spinning of the slot machine.
 */
function repeat() {
  outputText.innerHTML += "Please wait...<br>";
  terminal.scrollTop = terminal.scrollHeight;
  winner = null;
  button2.disabled = true;

  const intervalId = setInterval(() => {
    if (winner !== null) {
      clearInterval(intervalId);
      return;
    }
    spin();
  }, 6000);
}

/**
 * Displays an alert with a given message.
 * @param {string} message - The message to display in the alert.
 */
function showAlert(message) {
  const alert = document.createElement('div');
  alert.textContent = message;
  alert.classList.add('alert');
  document.body.appendChild(alert);
  setTimeout(() => {
    alert.remove();
    button2.disabled = false;
  }, 3000);
}

/**
 * Checks conditions after a spin and shows appropriate alerts.
 * @param {string} winner - The winner of the spin.
 * @param {boolean} elimination - Whether elimination mode is enabled.
 */
function checkConditions(winner, elimination) {
  if (winner && !elimination) {
    showAlert('Congratulations!');
  } else if (winner && elimination) {
    showAlert('You lost!');
  }
}
