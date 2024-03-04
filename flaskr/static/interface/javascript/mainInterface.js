window.onload = function f(){
    let id_first_row = document.getElementById('first-row');
    if (id_first_row != null){
        //exists
        $("#button_dashboard").hide();
    }else{
        $("#button_dashboard").show();
    }
    //alert_autodismiss();
}

function alert_autodismiss(){
    let alert_list = document.querySelectorAll('.alert')
    alert_list.forEach(function(alert) {
        new bootstrap.Alert(alert);

        let alert_timeout = 5000;
        setTimeout(() => {
            bootstrap.Alert.getInstance(alert).close();
        }, +alert_timeout);
    });
}