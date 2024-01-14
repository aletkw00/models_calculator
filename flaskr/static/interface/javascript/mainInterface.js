window.onload = function f(){
    let id_first_row = document.getElementById('first-row');
    if (id_first_row != null){
        //exists
        $("#button_dashboard").hide();
    }else{
        $("#button_dashboard").show();
    }
}