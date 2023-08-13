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

// Show the list of uploaded files
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('file-list');

fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    displayFileNames(files);
});

function displayFileNames(files) {
    fileList.innerHTML = '';
    for (const file of files) {
        const listItem = document.createElement('div');
        listItem.textContent = file.name;
        fileList.appendChild(listItem);
    }
}