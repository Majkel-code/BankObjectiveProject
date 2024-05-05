
const regUser_Name = document.getElementById('reg-name');
const regUser_Surname = document.getElementById('reg-surname');
const regUser_Pesel = document.getElementById('reg-pesel');
const regUser_Email = document.getElementById('reg-email');
const regUser_Password = document.getElementById('reg-password');
const regUser_repPassword = document.getElementById('reg-password-repeat');
const sendRegUser = document.getElementById("showToast");
const popup = document.querySelector(".popup-showToast");
const popupMsg = document.querySelector(".popup-showToast>p");
const closeMsg = document.querySelector(".popup-showToast>.close-Toast")

const mainRegisterBtn = document.querySelector(".registry-button");
const registerContekst = document.querySelector(".popup-container>.register")

class RegisterUser extends LoginRegistryConstructor {
    constructor() {
        super();
    };

    RegisterPopupDisplay(){
        this.popupDisplay();
        registerContekst.classList.add("active");
      };

    registerPopupClose(){
        this.PopupClose();
        registerContekst.classList.remove("active");
        this.registerClear();
      };

    registerClear(){
        regUser_Name.value = ""
        regUser_Surname.value = ""
        regUser_Pesel.value = ""
        regUser_Email.value = ""
        regUser_Password.value = ""
        regUser_repPassword.value = ""
    }

    async checkRegisterData(){
        this.checkForm([regUser_Name,regUser_Surname, regUser_Pesel, regUser_Password, regUser_repPassword, regUser_Email]);
        this.checkLength(regUser_Name, 3);
        this.checkLength(regUser_Surname,3);
        this.checkLength(regUser_Password, 8);
        this.checkPesel(regUser_Pesel);
        this.checkPassword(regUser_Password, regUser_repPassword);
        this.checkMail(regUser_Email);
        if (this.checkError()){
            this.acc_id = this.generateAccId();
            this.acc_number = this.generateAccNumber();
            console.log(this.acc_number);
            this.password = regUser_Password.value;
            this.name = regUser_Name.value;
            this.surname = regUser_Surname.value;
            this.pesel = regUser_Pesel.value;
            this.email = regUser_Email.value;
            const request_register = await this.userRegisterSent();
            console.log(request_register)
            if(request_register["STATUS"]){
                popup.classList.add("show-popup");
                popupMsg.textContent = "Formularz został poprawnie wysłany!";
            }
            else if(!request_register["STATUS"]){
                popup.classList.add("show-popup");
                popupMsg.textContent = `${request_register["ERROR"]}`;
            }
            else{
                popup.classList.add("show-popup");
                popupMsg.textContent = "Oops! There was some internal error!";
            }
            this.registerPopupClose();
            this.registerClear();
        }    
    };

    async userRegisterSent(){

        const data = {
          acc_id: this.acc_id,
          acc_number: this.acc_number,
          password: this.password,
          name: this.name,
          surname: this.surname,
          pesel: this.pesel,
          email: this.email,
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
    
        const request_connect = await fetch("http://127.0.0.1:5000/register", requestOptions);
        if (request_connect.ok) {
          let response = await request_connect.json()
          console.log(response)
          return response
        }
      }

      CloseMsgPopup(){
        registerContekst.classList.remove("active");
        popup.classList.remove("show-popup");
        this.registerPopupClose();
      }
}
const user_registry = new RegisterUser();

mainRegisterBtn.addEventListener("click", ()=>{
    user_registry.RegisterPopupDisplay()
  })

closePopup.addEventListener("click", ()=>{
    user_registry.registerPopupClose()
  })

sendRegUser.addEventListener("click",e =>{
	e.preventDefault();
    user_registry.checkRegisterData();
})
closeMsg.addEventListener("click", ()=>{
    user_registry.CloseMsgPopup();
})
