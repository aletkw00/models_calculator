
window.onload = function f(){
    document.getElementById('button_update').disabled = true;
    form_listener();
}

function form_listener(){
    let email = document.getElementById('field_email');
    let password = document.getElementById('field_password');
    email.addEventListener('input', function(){
        document.getElementById('button_update').disabled = false;
    });
    password.addEventListener('input', function(){
        document.getElementById('button_update').disabled = false;
    });
}