const btn = document.getElementById('menu-btn')
const nav = document.getElementById('menu')


btn.addEventListener('click', () =>{
    btn.classList.toggle('open')
    nav.classList.toggle('flex')
    nav.classList.toggle('hidden')
})



function myFunction(){
    var x = document.getElementById("show-password");
    
    if(x.type === "password"){
        x.type = "text";
    }else{
        x.type = "password";
    }
}

function myFunction2(){
    var x = document.getElementById("show-password2");
    
    if(x.type === "password"){
        x.type = "text";
    }else{
        x.type = "password";
    }
}




