// JavaScript code to send a logout request to Flask

// Function to send the logout request
function consumer_logout() {
    fetch('/auth/logout/', {
        method: 'POST',
    })
        .then(response => {
            if (response.ok) {
                // Redirect the user to the login page or perform any desired action
                window.location.href = '/auth/signin/';
            } else {
                console.error('Logout request failed.');
            }
        })
        .catch(error => {
            console.error('Error occurred while sending logout request:', error);
        });
}

