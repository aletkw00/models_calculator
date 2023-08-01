document.getElementById('addData').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    var formData = new FormData(this);

    // Create a new XMLHttpRequest object
    var xhr = new XMLHttpRequest();

    // Configure the request
    xhr.open('POST', '/modal', true);

    // Set the onerror callback function
    xhr.onerror = function() {
        console.error('Request failed');
    };

    // Set the onload callback function
    xhr.onload = function() {
        // Check if the request was successful
        if (xhr.status === 200) {
            // Request was successful, handle the response
            var response = JSON.parse(xhr.responseText);
            var status = response.status;
            var message = response.message;

            if (status === 'success') {
                // Request succeeded, perform actions if needed
                alert(message);
                // Additional actions if needed

                // Close the modal
                $('#add_data_Modal').modal('hide');
            } else {
                // Request failed, display the error message
                alert(message);
            }
        } else {
            // Request failed, handle the error
            console.error('Request failed with status ' + xhr.status);
        }
    };

    // Send the request with the form data
    xhr.send(formData);
});