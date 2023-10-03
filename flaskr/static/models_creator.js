// If user click on element model_dir_input then call showModelDirList()
document.getElementById('model_dir').addEventListener('click', showModelDirList);

// Show the list of dir
function showModelDirList() {
    document.getElementById('model_dir_list').style.display = 'block';
}

// Set the value of model_dir_input then close the list of dir
function selectModelDir(dir) {
    document.getElementById('model_dir').value = dir;
    document.getElementById('model_dir_list').style.display = 'none';
}

function updateFileName(inputId) {
    const input = document.getElementById(inputId);
    const fileName = input.files[0] ? input.files[0].name : ''; // Ottieni il nome del primo file o una stringa vuota
    const label = input.nextElementSibling; // Ottieni l'etichetta successiva all'input

    label.innerHTML = fileName;
}

function updateFileNames(inputId) {
    const input = document.getElementById(inputId);
    const fileNames = Array.from(input.files).map(file => file.name).join(', ');
    const label = input.nextElementSibling; // Ottieni l'etichetta successiva all'input

    label.innerHTML = fileNames || 'Choose files';
}

// Print the messagge 'Processing...' in the div 'output'
function showProcessing() {
    document.getElementById("output").innerHTML = "Processing...";
}

// Save or Delete button
function handleAction(action, event) {
    // Get the values from input fields
    var modelDir = document.querySelector('input[name="model_dir"]').value;
    var hostname = document.querySelector('input[name="host_name"]').value;
    var password = document.querySelector('input[name="password"]').value;
    var IP = document.querySelector('input[name="IP"]').value;
    var topic = document.querySelector('input[name="topic"]').value;
    

    var outputContent = document.getElementById('output').innerHTML;

    // Determine the endpoint based on the action
    var endpoint = action === 'save' ? '/saving' : '/delete';

    // Prepare the payload based on the action
    var payload = {
        model_dir: modelDir,
        hostname: hostname,
        password: password,
        IP: IP,
        topic:topic,
        output_content: outputContent
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
            location.reload()
                
        } else {
            // Show error message without clearing input fields
            alert('Error: ' + message);
        }       
        
    };

    xhr.send(JSON.stringify(payload));
    event.preventDefault();
}