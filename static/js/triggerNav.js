function toggleNav() {
    // toggle landing page nav
    document.getElementById('mobile_nav').classList.toggle('hidden');
    document.getElementById('menu_open').classList.toggle('hidden');
    document.getElementById('menu_close').classList.toggle('hidden');
}


function toggle_DashBoard() {
    // toggle dashboard nav
    obj = document.getElementById('Dashboard')
    obj.classList.toggle('hidden');
    obj.classList.toggle('absolute');
    obj.classList.toggle('top-20');
}

function toggle_Buy_Option() {
    // show dialog box to buy 
    
}