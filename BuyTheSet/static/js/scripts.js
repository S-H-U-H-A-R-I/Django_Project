// Function to display the alert message
function displayAlert(message, alertType) {
    // Create the alert element
    const alert = document.createElement('div');
    alert.classList.add('alert', `alert-${alertType}`, 'alert-dismissible', 'fade', 'show', 'cart-message', 'd-flex', 'justify-content-between', 'align-items-center', 'position-fixed', 'end-0', 'm-3', 'rounded');
    alert.setAttribute('role', 'alert');

    // Set the alert message
    const messageElement = document.createElement('p');
    messageElement.classList.add('mb-0', 'flex-grow-1');
    messageElement.textContent = message;

    // Create the close button
    const closeButton = document.createElement('button');
    closeButton.classList.add('btn-close');
    closeButton.setAttribute('type', 'button');
    closeButton.setAttribute('data-bs-dismiss', 'alert');
    closeButton.setAttribute('aria-label', 'Close');

    closeButton.addEventListener('click', () => {
        alert.remove();
    })

    // Append the message and close button to the alert
    alert.appendChild(messageElement);
    alert.appendChild(closeButton);

    // Append the alert to the page
    const alertContainer = document.getElementById('alert-container');
    if (alertContainer) {
        alertContainer.appendChild(alert);
    }

    // Remove the alert after 3 seconds
    setTimeout(() => {
        alert.classList.remove('show');
    }, 3000);
}







