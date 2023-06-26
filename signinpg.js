
function check(){
    console.log(username.value)
        sessionStorage.setItem("Username", username.value)
}
const username = document.getElementById('Uname')
console.log(username)
username.addEventListener("input", check);
/* document.getElementById('button') = ()=>{
    
    if(username != ''){
        alert(` welcome ${Username}`)
    }
} */