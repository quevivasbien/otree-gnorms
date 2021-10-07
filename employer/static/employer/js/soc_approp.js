// overwrites some of the functions in bidding.js

const buttons = document.getElementById('id_soc_approp_ratings').getElementsByTagName('input');

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
