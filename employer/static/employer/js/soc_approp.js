// overwrites some of the functions in bidding.js

const buttons = document.getElementById('id_soc_approp_ratings').getElementsByTagName('input');
const no_response_message = document.getElementById('no-response-message');

function updateInputDisplay() {
    let value = playerBids.value.split('-')[currentTab - 1];
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].checked = (value == i);
    }
}

function sendEntry() {
    for (let i = 0; i < buttons.length; i++) {
        if (buttons[i].checked) {
            let bids = playerBids.value.split('-');
            bids[currentTab-1] = i;
            playerBids.value = bids.join('-');
            return true;
        }
    }
    return false;
}

function forward() {
    if (sendEntry()) {
        forwardTab();
        no_response_message.style.display = 'none';
    }
    else {
        no_response_message.style.display = 'block';
    }
}

function back() {
    if (currentTab > numApplicants) {
        show('questions', 'finished');
        currentTab--;
    }
    else {
        sendEntry();
        backTab();
        no_response_message.style.display = 'none';
    }
}
