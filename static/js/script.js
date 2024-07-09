var sidebarOpen = false;
var sidebar = document.getElementById("sidebar");

function openSidebar() {
    if (!sidebarOpen) {
        sidebar.classList.add("sidebar-responsive");
        sidebarOpen = true;
        document.addEventListener('click', outsideClickListener);
    }
}

function closeSidebar() {
    if (sidebarOpen) {
        sidebar.classList.remove("sidebar-responsive");
        sidebarOpen = false;
        document.removeEventListener('click', outsideClickListener);
    }
}

function outsideClickListener(event) {
    if (!sidebar.contains(event.target) && sidebarOpen) {
        closeSidebar();
    }
}
