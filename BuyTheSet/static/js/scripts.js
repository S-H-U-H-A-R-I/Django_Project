function displayAlert(message, alertType) {
    const alertContainer = document.getElementById('alert-container');
    const alertElement = document.createElement('div');
    alertElement.classList.add('alert', `alert-${alertType}`, 'cart-message', 'pt-2', 'pb-3');
    alertElement.setAttribute('role', 'alert');
    alertElement.setAttribute('data-bs-autohide', 'true');
    alertElement.innerHTML = `
        <p class="mb-0">${message}</p>
        <div class="progress position-absolute bottom-0 start-0 end-0 mx-3 mb-1" style="height: 5px;">
            <div class="progress-bar custom-bg-${alertType}" role="progressbar" style="width: 100%;" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"></div>
        </div>
    `;
    alertContainer.appendChild(alertElement);

    // Start the progress bar animation
    const progressBar = alertElement.querySelector('.progress-bar');
    let width = 100;
    const animationDuration = 5000;
    const animationInterval = 30;
    const animationStep = (100 / animationDuration) * animationInterval;

    const animationTimer = setInterval(() => {
        if (width <= 0) {
            clearInterval(animationTimer);
            alertElement.remove();
        } else {
            width -= animationStep;
            progressBar.style.width = width + '%';
        }
    }, animationInterval);

    // Remove the alert when the user navigatest away from the page
    window.addEventListener('beforeunload', () => {
        alertElement.remove();
    });
}








