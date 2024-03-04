
let timer;

window.onload = function f(){
    document.getElementById('submit_button').disabled = true;
    form_listener();
    setup_timer();
    start();
}


function start(){
    let phase = document.getElementById('process_phase');
    if (phase.innerHTML == '2'){
        // phase 2
        // submit ok, start run from javascript
        $("#before_result_uploading_ok").show();
        $("#before_result_processing_bar").hide();
        $("#result_body").hide();
        $("#result_body_output_body").hide();
        startProcess()
    }else if (phase.innerHTML == '1') {
        // phase 1
        // submit with error
        $("#before_result_uploading_error").show();
        $("#before_result_processing").hide();
        $("#result_body").hide();
    } else {
        // phase 0
        // before submit and run 
        $("#before_result_uploading").hide();
        $("#before_result_processing").hide();
        $("#result_body").hide();
    }
}


function showUploading() {
    $("#before_result_uploading").show();
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


function process_output(output){
    $("#result_body_output_body").show();
    document.getElementById("result_body_output").innerHTML = output;
}


function message_saved(dir,name){
    let text = "All result files start with \""
    let text2 = "\" and are saved in folder \""
    let text3 = "\""
    document.getElementById("result_body_message").innerHTML = text.concat(name, text2, dir, text3);
}


function message_error(msg){
    $("#result_body_buttons").hide();
    document.getElementById("result_body_message").innerHTML = 'ERRORE: ' + msg;
}


function startProcess() {
    this.timer.start();
    $("#before_result_processing_bar").show();
    let that = this;

    let window = document.getElementById("process_data_window").innerText;
    let test = (/True/).test(document.getElementById("process_data_test").innerText);

    var payload = {
        window: window,
        test: test,
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/regression_calculator/run', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        try {
            var response = JSON.parse(xhr.responseText);
        } catch (error) {
            message_error(error);
            $("#before_result_processing_bar").hide();
            $("#result_body").show();
            that.timer.stop();
            return;
        }
        let dir = "";
        let name = "";
        Object.keys(response).forEach(function(key){
            if (key == 'directory'){
                dir = response[key];
            };
            if (key == 'filename'){
                name = response[key];
            };
            if (key == 'output'){
                process_output(response[key]);
            };
            if (key == 'error'){
                message_error('http ' + response[key]);
            };
        });
        if (dir != ''){
            message_saved(dir,name);
        }
        $("#before_result_processing_bar").hide();
        $("#result_body").show();
        that.timer.stop();
    }

    xhr.send(JSON.stringify(payload));

}

function setup_timer(){
    this.timer = new _timer();
    this.timer.reset();
}

function _timer(callback)
{
    var time = 0;     //  The default time of the timer
    var status = 0;    //    Status: timer is running or stoped
    var timer_id;    //    This is used by setInterval function
    
    // this will start the timer ex. start the timer with 1 second interval timer.start(1000) 
    this.start = function(interval){
        interval = 1000;
        
        if(status == 0){
            status = 1;
            timer_id = setInterval(function(){
                time++;
                generateTime();
                if(typeof(callback) === 'function') callback(time);
            }, interval);
        }
    }
    
    //  Same as the name, this will stop or pause the timer ex. timer.stop()
    this.stop =  function(){
        if(status == 1){
            status = 0;
            clearInterval(timer_id);
        }
    }
    
    // Reset the timer to zero or reset it to your own custom time ex. reset to zero second timer.reset(0)
    this.reset =  function(sec){
        sec = (typeof(sec) !== 'undefined') ? sec : 0;
        time = sec;
        generateTime(time);
    }
    
    // This methode return the current value of the timer
    this.getTime = function()
    {
        return time;
    }
    
    // This methode return the status of the timer running (1) or stoped (1)
    this.getStatus
    {
        return status;
    }
    
    // This methode will render the time variable to hour:minute:second format
    function generateTime()
    {
        var second = time % 60;
        var minute = Math.floor(time / 60) % 60;
        var hour = Math.floor(time / 3600) % 60;
        
        second = (second < 10) ? '0'+second : second;
        minute = (minute < 10) ? '0'+minute : minute;
        hour = (hour < 10) ? '0'+hour : hour;
        
        $('div.timer span.second').html(second);
        $('div.timer span.minute').html(minute);
        $('div.timer span.hour').html(hour);
    }
}