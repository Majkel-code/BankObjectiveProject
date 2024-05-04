const loginBtn = document.getElementById('btn1');
const userIdInput = document.getElementById('login-user-number');
const passwordInput = document.getElementById('login-password');

const mainLoginBtn = document.querySelector(".login-button");
const actionPopup = document.querySelector(".popup-container");

const loginContekst = document.querySelector(".popup-container>.login")
const contentHider = document.querySelector(".hide-content");
const closePopup = document.querySelector(".close-popup");

const errorMsg = document.querySelector(".login>.error-msg");

class LoginUser extends LoginRegistryConstructor{
    constructor() {
      super();
      this.acc_id = null;
      this.password = null;
    }

    registerClear(){
      userIdInput.value = "99999"
      passwordInput.value = "testpassword"
    }
  
    async userLoginSent(){

      const data = {
        acc_id: this.acc_id,
        password: this.password,
        };

      const jsonData = JSON.stringify(data);
      console.log(jsonData)
      let requestOptions = {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json' 
          },
          redirect: 'follow',
          body: jsonData,
          
        };
  
      const request_connect = await fetch("http://127.0.0.1:5000/login", requestOptions);
      if (request_connect.ok) {
        let response = await request_connect.json()
        console.log(response)
        return response
      }
    }

    reloadErrorPage(){
      errorMsg.textContent = "Incorrect login details";
      errorMsg.classList.add("show");
    }

    LoginPopupDisplay(){
      this.popupDisplay()
      loginContekst.classList.add("active")
    }

    loginPopupClose(){
      this.PopupClose();
      loginContekst.classList.remove("active");
      this.registerClear();
    }

}
const user_login = new LoginUser();
async function processUser(){
    if (userIdInput.value != "" && passwordInput.value != ""){
        response_err = await user_login.checkProperties(user_id=userIdInput.value, password=passwordInput.value);
        if (response_err["STATUS"]){
          user_login.dataToLoad = response_err["DATA"];
          user_login.saveData();
          window.open("dashboard.html", '_self');
          
          // window.location.href = 'dashboard.html';
          console.log("LOGIN->")
        }
        else{
          user_login.reloadErrorPage();
        }
      }
}
loginBtn.addEventListener('click', function() {
    processUser();
});

mainLoginBtn.addEventListener("click", ()=>{
  user_login.LoginPopupDisplay()
})

closePopup.addEventListener("click", ()=>{
  user_login.loginPopupClose()
})
