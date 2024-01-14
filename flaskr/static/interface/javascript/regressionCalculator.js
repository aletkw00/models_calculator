//let regression_form = document.getElementById("uploadForm");
//loginForm.addEventListener("submit", (e) => {
//    e.preventDefault();
//});

window.onload = function f(){
    document.getElementById('submit_button').disabled = true;
    start();
    form_listener();
}


function start(){
    let result = document.getElementById('result_regression');
    if (result.value == ''){
        //no execution
        $("#before_result").hide();
        $("#result_real").hide();
        $("#buttons_result").hide();
    }else{
        $("#before_result").hide();
        $("#result_real").show();
        $("#buttons_result").show();
        saveFile();
    }
}


function form_listener(){
    let myform = document.getElementById('uploadForm');
    myform.addEventListener('input', function(){
        if (myform.checkValidity()){
            document.getElementById('submit_button').disabled = false;
        }else{
            document.getElementById('submit_button').disabled = true;
        }
    });
}


// Set the value of model_dir_input
function selectModelDir(dir) {
    document.getElementById('field_model_dir').value = dir;
}


function updateFileInput() {
    let input = document.getElementById("field_file_input");
    let fileName = input.files[0] ? input.files[0].name : ''; // Ottieni il nome del primo file o una stringa vuota
    let label = input.nextElementSibling; // Ottieni l'etichetta successiva all'input

    label.innerHTML = fileName;
}


function updateFilesOutput() {
    let input = document.getElementById("field_files_output");
    let fileNames = Array.from(input.files).map(file => file.name).join(', ');
    let label = input.nextElementSibling; // Ottieni l'etichetta successiva all'input

    label.innerHTML = fileNames || 'Choose files';

    // edit height of elements to fit content
    let newheight = label.offsetHeight.toString().concat("px");
    document.getElementById('field_files_output').style.height = newheight ;
    document.getElementById('container_field_files_output').style.height = newheight;
}


function showProcessing() {
    $("#before_result").show();
    $("#result_real").hide();
    $("#buttons_result").hide();
}


function message_saved(dir,name){
    let text = "All file result start with \""
    let text2 = "\" and are saved in folder \""
    let text3 = "\""
    document.getElementById("text_result").innerHTML = text.concat(name, text2, dir, text3);
}


function saveFile() {
    var payload = {
        //modelDir: document.getElementById("input_model_dir").value,
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/regression_calculator/save', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        try {
            var response = JSON.parse(xhr.responseText);
        } catch (error) {
            return {'Error': true};
        }
            let dir = "";
            let name = "";
            Object.keys(response).forEach(function(key){
                if (key == 'directory'){
                    dir = response[key];
                }                
                if (key == 'filename'){
                    name = response[key];
                };
            });
            if (dir != ''){
                message_saved(dir,name);
            }
    }

    xhr.send(JSON.stringify(payload));

}
