// Check the window field to be an integer and not < 0
function validateForm(event, showProcessing) {
    var windowInput = document.getElementById("window_input");
    var windowError = document.getElementById("window_error");
    


    var windowValue = parseInt(windowInput.value); // Converto il valore in un intero

    if ((windowInput.value != '' & isNaN(windowValue)) || windowValue < 0) {
        windowError.style.display = "block";
        event.preventDefault();  // Previeni l'invio del modulo
    } else {
        windowError.style.display = "none";
        if (showProcessing) {
            showProcessing();
            
        }
    }
}

// Print the messagge 'Processing...' in the div 'output'
function showProcessing() {
    document.getElementById("output").innerHTML = "Processing...";
}


document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    // Get all input value from form 'uploadForm'
    var formData = new FormData(this);

    // Create a new XMLHttpRequest object
    var xhr = new XMLHttpRequest();

    // Configure the request
    xhr.open('POST', '/models_creator', true);

    // Set the response type
    xhr.responseType = 'json';

    // Set the onload callback function
    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = xhr.response;
            var outputElement = document.getElementById('output');
            outputElement.innerHTML = response.message.replace(/\n/g, '<br>');
        } else {
            console.error('Request failed. Status:', xhr.status);
        }
    };

    // Set the onerror callback function
    xhr.onerror = function() {
        console.error('Request failed');
    };

    // Send the request with the form data
    xhr.send(formData);
});

// Save or Delete button
function handleAction(action) {
    // Get the values from input fields
    var modelDir = document.querySelector('input[name="model_dir"]').value;
    var filename = document.querySelector('input[name="filename"]').value;
    var hostname = document.querySelector('input[name="host_name"]').value;
    var password = document.querySelector('input[name="password"]').value;
    var IP = document.querySelector('input[name="IP"]').value;
    var topic = document.querySelector('input[name="topic"]').value;

    // Determine the endpoint based on the action
    var endpoint = action === 'save' ? '/saving' : '/delete';

    // Prepare the payload based on the action
    var payload = {
        model_dir: modelDir,
        filename: filename,
        hostname: hostname,
        password: password,
        IP: IP,
        topic:topic
    };

    var xhr = new XMLHttpRequest();
    xhr.open('POST', endpoint, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function() {
        var response = JSON.parse(xhr.responseText);
        var status = response.status;
        var message = response.message;

        // Show alert based on the status
        if (status === 'success') {
            // Clear all input fields
            var inputFields = document.querySelectorAll('input');
            inputFields.forEach(function(input) {
                input.value = '';
            });

            // Reload the page after the request is completed
            location.reload();
            
        } else {
            // Show error message without clearing input fields
            alert('Error: ' + message);
        }       
        
    };

    xhr.send(JSON.stringify(payload));
}
