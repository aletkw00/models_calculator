// If user click on element model_dir_input then call showModelDirList()
document.getElementById('model_dir_input').addEventListener('click', showModelDirList);

// Show the list of dir
function showModelDirList() {
    document.getElementById('model_dir_list').style.display = 'block';
}

// Set the value of model_dir_input then close the list of dir
function selectModelDir(dir) {
    document.getElementById('model_dir_input').value = dir;
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