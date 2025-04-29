document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('feedback-form-container');
    var btn = document.getElementById('feedback-button');
    var span = document.getElementsByClassName('close')[0];

    // Toggle the display of the modal when the button is clicked
    btn.onclick = function() {
        modal.style.display = modal.style.display === 'block' ? 'none' : 'block';
    };

    // Close the modal when the close (x) button is clicked
    span.onclick = function() {
        modal.style.display = 'none';
    };

    // Close the modal when the user clicks anywhere outside of it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };

    var sendButton = document.getElementById('send-button');

    // Add an event listener to the send button
    sendButton.addEventListener('click', function() {
        // Close the modal when the send button is clicked
        modal.style.display = 'none';
    });
});
