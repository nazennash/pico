document.addEventListener('DOMContentLoaded', function() {
    // Example: Adding an event listener to a button
    const streamButton = document.getElementById('start-stream');
    if (streamButton) {
        streamButton.addEventListener('click', function() {
            alert('Stream started!');
        });
    }
    
    // Example: Toggle visibility of an element
    const toggleButton = document.getElementById('toggle-section');
    const section = document.getElementById('section-to-toggle');
    
    if (toggleButton && section) {
        toggleButton.addEventListener('click', function() {
            section.classList.toggle('hidden');
        });
    }
});
