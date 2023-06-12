function toggleNav() {
    // toggle landing page nav
    document.getElementById('mobile_nav').classList.toggle('hidden');
    document.getElementById('menu_open').classList.toggle('hidden');
    document.getElementById('menu_close').classList.toggle('hidden');
}


function toggle_Consumer_DashBoard() {
    // toggle dashboard nav
    var obj = document.getElementById('Consumer_Dashboard');
    obj.classList.toggle('hidden');
    obj.classList.toggle('absolute');
    obj.classList.toggle('top-20');
}

function toggle_Producer_DashBoard() {
    // toggle dashboard nav
    var obj = document.getElementById('Producer_Dashboard');
    obj.classList.toggle('hidden');
    obj.classList.toggle('absolute');
    obj.classList.toggle('top-20');
}

function toggle_Aggregator_DashBoard() {
    // toggle dashboard nav
    var obj = document.getElementById('Aggregator_Dashboard');
    obj.classList.toggle('hidden');
    obj.classList.toggle('absolute');
    obj.classList.toggle('top-20');
}

function toggle_Buy_Option() {
    // show dialog box to buy 
    var buyDialogBox = document.getElementById('buyDialogBox');
    buyDialogBox.classList.toggle('opacity-0');
    buyDialogBox.classList.toggle('pointer-events-none');
}

// close pop up by redirecting to normal endpoint (/user/consumer/monitor)
function closeBuyPopUp() {
    window.location.href = "/user/consumer/monitor";
}

function toggle_Sell_Option() {
    // show dialog box to buy 
    var buyDialogBox = document.getElementById('sellDialogBox');
    buyDialogBox.classList.toggle('opacity-0');
    buyDialogBox.classList.toggle('pointer-events-none');
}

// close pop up by redirecting to normal endpoint (/user/consumer/monitor)
function closeBuyPopUp() {
    window.location.href = "/user/consumer/monitor";
}

function toggleAggregator(selected) {
    var option = document.getElementById('aggregatorOption');
    if (selected.options[selected.selectedIndex].text == "Aggregator") {
        option.classList.add('hidden');
    } else {
        option.classList.remove('hidden');
    }
}