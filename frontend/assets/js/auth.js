function isAuthenticated() {
    return !!localStorage.getItem('token');
}

function getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.width = '/frontend/index.html';
}

function checkAuthGuard(role = null) {
    if (!isAuthenticated()) {
        window.location.href = '/frontend/login.html';
        return;
    }

    if (role) {
        const user = getUser();
        if (user.role !== role) {
            alert("Warning: Unauthorized access. Redirecting...");
            if (user.role === 'admin') window.location.href = '/frontend/admin_dashboard.html';
            else window.location.href = '/frontend/client_dashboard.html';
        }
    }
}
