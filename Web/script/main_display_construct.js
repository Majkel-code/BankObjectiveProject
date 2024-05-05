class LoginRegistryConstructor extends MultiPageBridge{
    constructor() {
      super();
      localStorage.clear();
    //   this.checkIsUserLogout();
      this.acc_id = null;
      this.acc_number = null;
      this.password = null;
      this.name = null;
      this.surname = null;
      this.pesel = null;
      this.email = null;
      this.rep_password = null;
    }

    // checkIsUserLogout(){
    //     if (localStorage.logout){
    //         console.log("HERE!!!")
    //         localStorage.clear();
    //     }
    // }

    async checkProperties(user_id, password){
        if (user_id != "" && password != "" && (password).length >= 8){
            this.acc_id = user_id
            this.password = password
            let check_user = await this.userLoginSent()
            return check_user
            
        }
    };

    showError(input, msg){
        const formBox = input.parentElement;
        const errorMsg = formBox.querySelector(".error-text");
    
        formBox.classList.add("error");
        errorMsg.textContent = msg;
    };

    clearError (input) {
        const formBox = input.parentElement;
        formBox.classList.remove("error");
    };

    checkForm(input){
        input.forEach(el => {
            if (el.value === "") {
                this.showError(el, el.placeholder);
            } else {
                this.clearError(el);
            }
        });
    };
    
    checkLength(input, min){
        if (input.value.length < min) {
            const inputError = input.previousElementSibling.innerText.slice(0, -1);
            this.showError(input, `wartość '${inputError}' powinna składać się z min. ${min} znaków.`);
            return false;
        }
    };
    
    checkPassword(regUser_Password, regUser_repPassword){
        if (regUser_Password.value !== regUser_repPassword.value) {
            this.showError(regUser_repPassword, "Hasła do siebie nie pasują");
        }
    };

    checkPesel(pesel){
        const nums = /^\d+$/;
        if (nums.test(pesel.value)){
            if(this.checkLength(pesel, 11)){
                this.clearError(pesel);
            }  
        }
        else{
            this.showError(pesel, "PESEL może zawierać jedynie cyfry");
        }
    }
    
    checkMail(email) {
        const re =
            /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    
        if (re.test(email.value)) {
            this.clearError(email);
        } else {
            this.showError(email, "e-mail jest niepoprawny");
        }
    };
    
    checkError(){
        const allInputs = document.querySelectorAll(".form-box");
        let errorCount = 0;
    
        allInputs.forEach(el => {
            if (el.classList.contains("error")) {
                errorCount++;
            }
        });
        if (errorCount === 0) {
            return true
        }
        else{
            return false
        }
    };

    generateAccId(){
        let acc_id =  Math.floor(Math.random() * (99999 - 10000 + 1)) + 10000;
        if (acc_id == 99999){
            this.generateAccId();
        };
        return acc_id
    }

    generateAccNumber(){
        let acc_number = ""
        for (let i of Array(4).keys()) {
            acc_number = acc_number + String(Math.floor(Math.random() * (9999 - 1000 + 1)) + 1000);
            console.log(acc_number)
        }
        return acc_number
    }

    popupDisplay(){
        actionPopup.classList.add("active");
        contentHider.classList.add("active");
      }

      PopupClose(){
        actionPopup.classList.remove("active");
        contentHider.classList.remove("active");
      }
  
}
const constructor = new LoginRegistryConstructor();
