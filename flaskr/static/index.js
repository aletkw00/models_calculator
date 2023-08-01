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