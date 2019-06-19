$(document).ready(function(){

    $('.tabs').tabs({swipeable: false});
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $(".dropdown-trigger").dropdown({hover:true});
});
function check(Form_Name, password,confirm_password)
    {
//        alert('check');

        var email = $('#email').val();
        var reg = /^([\w-\.]+@(?!gmail123.com)(?!yahoo.com)(?!hotmail.com)(?!yahoo.co.in)(?!aol.com)(?!abc.com)(?!xyz.com)(?!pqr.com)(?!rediffmail.com)(?!live.com)(?!outlook.com)(?!me.com)(?!msn.com)(?!ymail.com)([\w-]+\.)+[\w-]{2,4})?$/;
        if (reg.test(email)){
//            return 0;
            var pass1 = document.getElementById(password).value;
            var pass2 = document.getElementById(confirm_password).value;
            if(pass2 != pass1){
                M.toast({html: 'Password Doesnt Match.'})
                return false;
            }
        }
        else{
            alert('Please Enter Business Email Address');
            return false;
        }
    }