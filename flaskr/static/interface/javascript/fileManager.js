//fonti
//https://stackoverflow.com/questions/20111219/display-bootstrap-modal-using-javascript-onclick
//https://stackoverflow.com/questions/62101647/javascript-bootstrap-open-bootstrap-modal-with-javascript-and-not-with-button
//https://www.geeksforgeeks.org/bootstrap-5-modal-via-javascript/
//https://stackoverflow.com/questions/15097315/change-onclick-attribute-with-javascript

let current_dir = null;
let previus_dir = null;
let left_list = null;
let right_list = null;
let new_input_name = '';

window.onload = function f(){
    start();
    modal_confimation();
}

function start(){
    getList('', 'START');
    $("#button_main").hide();    
    $("#select_folder").show();
    $("#button_download_folder").hide(); 
}

function modal_confimation(){
    let input = document.getElementById('confirmation_body_input');
    input.addEventListener('input', (event) =>{
        //console.log(event);
        //console.log(input.value);
        new_input_name = input.value;
        //console.log(new_input_name);
        if (new_input_name != ''){
            $("#confirmation_ok").prop('disabled', false);
            return;
        }
        $("#confirmation_ok").prop('disabled', true);
    });
}

function leftDirClick(dir) {
    getList(dir, 'LEFT');
    $("#button_main").show();    
    $("#select_folder").hide();
    $("#button_download_folder").show(); 
}

function rightDirClick(dir) {
    getList(dir, 'RIGHT');
}

function beforeDirClick(dir) {
    getList(dir, 'BEFORE');
}

function downloadFolder(dir){
    download(dir,true);
}

function downloadFile(dir){
    download(dir,false);
}

function message(text){
    $("#confirmation2_title").html('Information');
    $("#confirmation2_body_text1").html(text);
    $("#confirmation2_ok").html('Yes');
    $("#confirmation2_ok").off();
    $("#confirmation2_ok").hide();
    $("#confirmation2_no").html('Close');
    $('#confirmation2').modal('show');
}

function renameFolder(dir, list){
    let folderName = dir.split('/').pop();
    let input = document.getElementById('confirmation_body_input');
    input.value = '';
    input.placeholder = folderName;
    $("#confirmation_title").html('Rename confirmation');
    $("#confirmation_body_text1").html('Current folder name: "' + folderName + '".');
    $("#confirmation_body_text2").html('Type the new folder name.');
    $("#confirmation_body_text2").show();
    $("#confirmation_body_input").show();
    $("#confirmation_ok").html('Yes');
    $("#confirmation_ok").off();
    $("#confirmation_ok").prop('disabled', true);
    $("#confirmation_ok").on("click", function (){
        rename_fun(dir, new_input_name, true, list)
    });
    $("#confirmation_no").html('No - I keep it');
    $('#confirmation').modal('show');
}

function renameFile(dir){
    let fileName = dir.split('/').pop();
    let input = document.getElementById('confirmation_body_input');
    input.value = '';
    input.placeholder = fileName;
    $("#confirmation_title").html('Rename confirmation');
    $("#confirmation_body_text1").html('Current file name: "' + fileName + '".');
    $("#confirmation_body_text2").html('Type the new file name. (Keep same file extension)');
    $("#confirmation_body_text2").show();
    $("#confirmation_body_input").show();
    $("#confirmation_ok").html('Yes');
    $("#confirmation_ok").off();
    $("#confirmation_ok").prop('disabled', true);
    $("#confirmation_ok").on("click", function (){
        rename_fun(dir, new_input_name, false)
    });
    $("#confirmation_no").html('No - I keep it');
    $('#confirmation').modal('show');
}

function deleteFolder(dir, list){
    $("#confirmation_title").html('Delete confirmation');
    $("#confirmation_body_text1").html('Are you sure to delete "' + dir.split('/').pop() + '" folder and all its content ?');
    $("#confirmation_body_text2").hide();
    $("#confirmation_body_input").hide();
    $("#confirmation_ok").html('Yes');
    $("#confirmation_ok").off();
    $("#confirmation_ok").prop('disabled', false);
    $("#confirmation_ok").on("click", function (){
        delete_fun(dir,true, list)
    });
    $("#confirmation_no").html('No - I keep it');
    $('#confirmation').modal('show');
}

function deleteFile(dir){
    $("#confirmation_title").html('Delete confirmation');
    $("#confirmation_body_text1").html('Are you sure to delete "' + dir.split('/').pop() + '" ?');
    $("#confirmation_body_text2").hide();
    $("#confirmation_body_input").hide();
    $("#confirmation_ok").html('Yes');
    $("#confirmation_ok").off();
    $("#confirmation_ok").prop('disabled', false);
    $("#confirmation_ok").on("click", function (){
        delete_fun(dir,false)
    });
    $("#confirmation_no").html('No - I keep it');
    $('#confirmation').modal('show');
}

function reloadLeft(){
    right_list = null;
    rightList();
    current_dir = previus_dir;
    currentDirText();
    getList(current_dir, 'UPDATE-LEFT');
}


function reloadRight(){
    getList(current_dir, 'UPDATE-RIGHT');
}


//change current_dir_text
function currentDirText(){
    let DOMdirText = document.getElementById('current_dir_text');
    DOMdirText.textContent = current_dir;
}

//edit a LEFT LIST
function leftList() {

    let DOMleftlist = document.getElementById('left-list');
    DOMleftlist.replaceChildren();

    if (Object.keys(left_list).length == 0){
        var newItem = document.createElement('li');
        newItem.className = 'list-group-item';
        //first element           
        var iconItem = document.createElement('h5');
        //iconItem.className = 'bi-folder';
        iconItem.textContent = 'Empty';
        newItem.append(iconItem);
        DOMleftlist.appendChild(newItem);
    } else {
        Object.keys(left_list).forEach(function(key) {
            //true if is folder
            if (left_list[key]){
                var newItem = document.createElement('li');
                newItem.className = 'list-group-item';
                //first element           
                var iconItem = document.createElement('h5');
                iconItem.className = 'bi-folder';
                iconItem.textContent = ' ' + key;
                newItem.append(iconItem);
                //second element
                var listButton = document.createElement('span');
                var buttonOpenFolder = document.createElement('button');
                buttonOpenFolder.type = 'button';
                buttonOpenFolder.className = 'btn btn-info btn-sm list-button';
                var string_dir;
                if (current_dir == ''){
                    string_dir = previus_dir + key;
                }else{
                    string_dir = previus_dir + '//' + key;
                }
                buttonOpenFolder.setAttribute('onclick', 'leftDirClick(\'' + string_dir +'\')');            
                buttonOpenFolder.textContent = 'Open';
                var buttonRenameFolder = document.createElement('button');
                buttonRenameFolder.type = 'button';
                buttonRenameFolder.className = 'btn btn-warning btn-sm list-button';
                buttonRenameFolder.setAttribute('onclick', 'renameFolder(\''+ string_dir +'\', \'L\')');
                buttonRenameFolder.textContent = 'Rename';
                var buttonDeleteFolder = document.createElement('button');
                buttonDeleteFolder.type = 'button';
                buttonDeleteFolder.className = 'btn btn-danger btn-sm list-button';
                buttonDeleteFolder.setAttribute('onclick', 'deleteFolder(\''+ string_dir +'\', \'L\')');
                buttonDeleteFolder.textContent = 'X';
                listButton.append(buttonOpenFolder);
                listButton.append(buttonRenameFolder);
                listButton.append(buttonDeleteFolder);
                newItem.append(listButton);
                DOMleftlist.appendChild(newItem);
            }
        })
    }
}

//edit a RIGHT LIST
function rightList() {

    let DOMdownloadFolder = document.getElementById('button_download_folder');
    DOMdownloadFolder.setAttribute('onclick', 'downloadFolder(\'' + current_dir +'\')');

    let DOMrightlist = document.getElementById('right-list');
    DOMrightlist.replaceChildren();

    if (right_list == null){
        return;
    }

    if (Object.keys(right_list).length == 0){
        var newItem = document.createElement('li');
        newItem.className = 'list-group-item';
        //first element           
        var iconItem = document.createElement('h5');
        //iconItem.className = 'bi-folder';
        iconItem.textContent = 'Empty';
        newItem.append(iconItem);
        DOMrightlist.appendChild(newItem);
    } else {
        Object.keys(right_list).forEach(function(key) {        
            var newItem = document.createElement("li");
            newItem.className = 'list-group-item';
            if (right_list[key]){
                //if is a folder
                //first elementi
                var iconItem = document.createElement("h5");
                iconItem.className = 'bi-folder';
                iconItem.textContent = ' ' + key;
                newItem.append(iconItem);
                //second element
                var listButton = document.createElement('span');
                var buttonOpenFolder = document.createElement('button');
                buttonOpenFolder.type = 'button';
                buttonOpenFolder.className = 'btn btn-info btn-sm list-button';
                buttonOpenFolder.setAttribute('onclick', 'rightDirClick(\''+ current_dir + '/' + key+'\')');
                buttonOpenFolder.textContent = 'Open';
                var buttonDownloadFolder = document.createElement('button');
                buttonDownloadFolder.type = 'button';
                buttonDownloadFolder.className = 'btn btn-success btn-sm list-button';
                buttonDownloadFolder.setAttribute('onclick', 'downloadFolder(\''+ current_dir + '/' + key+'\')');
                buttonDownloadFolder.textContent = 'Download';
                var buttonRenameFolder = document.createElement('button');
                buttonRenameFolder.type = 'button';
                buttonRenameFolder.className = 'btn btn-warning btn-sm list-button';
                buttonRenameFolder.setAttribute('onclick', 'renameFolder(\''+ current_dir + '/' + key+'\', \'R\')');
                buttonRenameFolder.textContent = 'Rename';
                var buttonDeleteFolder = document.createElement('button');
                buttonDeleteFolder.type = 'button';
                buttonDeleteFolder.className = 'btn btn-danger btn-sm list-button';
                buttonDeleteFolder.setAttribute('onclick', 'deleteFolder(\''+ current_dir + '/' + key+'\', \'R\')');
                buttonDeleteFolder.textContent = 'Delete';
                listButton.append(buttonOpenFolder);
                listButton.append(buttonDownloadFolder);
                listButton.append(buttonRenameFolder);
                listButton.append(buttonDeleteFolder);
                newItem.append(listButton);
            } else {
                //if is a file
                //first elementi
                var iconItem = document.createElement("h5");
                iconItem.className = 'bi-file-earmark-text';
                iconItem.textContent = ' ' + key
                newItem.append(iconItem);
                //second element
                var listButton = document.createElement('span');
                var buttonDownloadFile = document.createElement('button');
                buttonDownloadFile.type = 'button';
                buttonDownloadFile.className = 'btn btn-success btn-sm list-button';
                buttonDownloadFile.setAttribute('onclick', 'downloadFile(\''+ current_dir + '/' + key+'\')');
                buttonDownloadFile.textContent = 'Download';
                var buttonRenameFile = document.createElement('button');
                buttonRenameFile.type = 'button';
                buttonRenameFile.className = 'btn btn-warning btn-sm list-button';
                buttonRenameFile.setAttribute('onclick', 'renameFile(\''+ current_dir + '/' + key+'\')');
                buttonRenameFile.textContent = 'Rename';
                var buttonDeleteFile = document.createElement('button');
                buttonDeleteFile.type = 'button';
                buttonDeleteFile.className = 'btn btn-danger btn-sm list-button';
                buttonDeleteFile.setAttribute('onclick', 'deleteFile(\''+ current_dir + '/' + key+'\')');
                buttonDeleteFile.textContent = 'Delete';
                listButton.append(buttonDownloadFile);
                listButton.append(buttonRenameFile);
                listButton.append(buttonDeleteFile);
                newItem.append(listButton);
            }
            DOMrightlist.appendChild(newItem);
        })
    }
}


//get list of files and directory
function getList(dir, type) {
    var payload = {
        insideDir: dir,
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/file_manager/getlist', false);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function() {
        try {
            var response = JSON.parse(xhr.responseText);
        } catch (error) {
            return {'Error': true}
        }
        if (type == 'LEFT'){
            right_list = response;
            previus_dir = current_dir;
            current_dir = dir
            currentDirText();
            rightList();
        }else if(type == 'RIGHT'){
            left_list = right_list;
            right_list = response;
            previus_dir = current_dir;
            current_dir = dir
            currentDirText();
            leftList();
            rightList();
        }else if(type == 'UPDATE-LEFT'){
            left_list = response;
            leftList();
        }else if(type == 'UPDATE-RIGHT'){
            right_list = response;
            rightList();            
        }else{
            left_list = response;
            right_list = null;
            current_dir = '';
            previus_dir = '';
            currentDirText();
            leftList();
            rightList();
        }
    };

    xhr.send(JSON.stringify(payload));
}


function download(path, isDir){
    var payload = {
        path: path,
        isDir: isDir
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/file_manager/get', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.responseType='blob'

    xhr.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            var blob = new Blob([this.response], {type: "application/octet-stream"});
            var file_name = xhr.getResponseHeader('Content-Disposition').split("filename=")[1];
            var url = window.URL.createObjectURL(blob);
            var link = document.createElement('a');
            link.href = url;
            link.download = file_name;
            link.click();
    
            setTimeout(() => {
            window.URL.revokeObjectURL(url);
            link.remove(); } , 100);
        }
        };

    xhr.send(JSON.stringify(payload));
}

function rename_fun(path, newname, isDir, list){
    var payload = {
        oldpath: path,
        newname: newname,
        isDir: isDir
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/file_manager/rename', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        try {
            var response = JSON.parse(xhr.responseText);
        } catch (error) {
            return {'Error': true}
        }
        result = Object.keys(response)
        returnName = response['name']
        //console.log(result)
        //console.log(response[result[0]])
        if (response[result[0]]){
            if (list == 'L'){
                previus_dir = '';
                reloadLeft();
            }else{
                reloadRight();
            }
            message('Rinominato con ' + newname);
        };
    };

    xhr.send(JSON.stringify(payload));

}

function delete_fun(path, isDir, list){
    var payload = {
        path: path,
        isDir: isDir
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/file_manager/delete', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        try {
            var response = JSON.parse(xhr.responseText);
        } catch (error) {
            return {'Error': true}
        }
        result = Object.keys(response)
        response[result[0]]
        //console.log(result)
        //console.log(response[result[0]])
        if (response[result[0]]){
            if (list == 'L'){
                reloadLeft();
            }else{
                reloadRight();
            }
        };
    };

    xhr.send(JSON.stringify(payload));

}