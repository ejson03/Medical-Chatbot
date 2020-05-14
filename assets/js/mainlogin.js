const {ipcRenderer} = require("electron");
require('dotenv').config();
const REST_API = process.env.REST_API;
(function ($) {
    "use strict";


    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
    
    function message(message){
        if(message == "user"){
            ipcRenderer.send("user")
        } else if (message == "admin"){
            ipcRenderer.send("user")
        } else {
            ipcRenderer.send("error")
        }
    }
    document.forms['login'].addEventListener('submit', async (event) => {
        event.preventDefault();
        let response = await fetch(`${REST_API}/login`, {
            method: 'POST',
            body: new URLSearchParams(new FormData(event.target))   
        });
        response = await response.json();
        console.log(response['message'])
        message(response['message']);
    });

    document.forms['register'].addEventListener('submit', async (event) => {
        event.preventDefault();
        let response = await fetch(`${REST_API}/signup`, {
            method: 'POST',
            body: new URLSearchParams(new FormData(event.target))   
        });
        response = await response.json();
        message(response['message']);
    });

})(jQuery);



