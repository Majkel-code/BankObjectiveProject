const DashboardMainPage = document.querySelector(".main-dashboard");
const profileInfo = document.querySelector(".profile-main>.profile-info");
const totalAmount = document.querySelector(".total-amount");
const lastTransactionContainer = document.querySelector(".new-deals-cards_list");

// nav buttons
const NavDashboardPage = document.querySelector(".dashboard-page");
const NavCreateTransfer = document.querySelector(".make-new-transfer");

// TRANSFER SECTION QUERY SELECTOR
const TransferContainer = document.querySelector(".new-transfer");
const TransferCloseBtn = document.querySelector(".dashboard-transfer-close-btn");
const TransferAccNumber = document.querySelector("#transfer-acc-number");
const TransferTitle = document.querySelector("#transfer-title");
const TransferAmount = document.querySelector("#transfer-amount");
const TransferDescription = document.querySelector("#transfer-description");
const TransferDate = document.querySelector("#transfer-date");

const sendTransferBtn = document.querySelector("#send-transfer");




class DashboardPage extends MultiPageBridge {
    constructor(){
        super();
    }

    setupConstruct(){
        let storage = this.loadLocalStorage();
        return storage
    }

    loadLocalStorage(){
        try {
            this.loggedUserData = JSON.parse(localStorage.myData);
        } catch (error) {
            return {"STATUS": false, "ERROR": "unable load data!"}
        }
        return {"STATUS": true, "ERROR": null}
    }


    async takeDataToLocalStorage(){
        const data = {
            acc_id: this.loggedUserData["ID"],
            };
    
          const jsonData = JSON.stringify(data);
          let requestOptions = {
              method: 'PATCH',
              headers: {
                'Content-Type': 'application/json' 
              },
              redirect: 'follow',
              body: jsonData,
              
            };
      
          const request_connect = await fetch("http://127.0.0.1:5000/login/take_data", requestOptions);
          if (request_connect.ok) {
            let response = await request_connect.json()
            if (response["STATUS"]){
                this.loggedUserData = response["DATA"]
            }
          }
    }


    loadProfileInfo(){
        let name_surname = profileInfo.children[0]
        name_surname.textContent = `${this.loggedUserData["NAME"]} ${this.loggedUserData["L_NAME"]}`;

        let acc_id_span = document.createElement("span");
        profileInfo.children[1].appendChild(acc_id_span);
        acc_id_span.innerText = `${this.loggedUserData["ID"]}`

        let acc_num_span = document.createElement("span");
        profileInfo.children[2].appendChild(acc_num_span);
        acc_num_span.innerText = `${this.loggedUserData["ACC_NUM"]}`;

    };
    getDayName(){
        let date = new Date();
        let date_day = date.getDate();
        let date_month = date.getMonth() + 1;
        let date_year = date.getFullYear();
        let day_namePL = date.toLocaleDateString("pl-PL", { weekday: 'long' });    
        let month_namePL = date.toLocaleDateString("pl-PL", { month: 'long' });

        totalAmount.querySelector("p").textContent = `${day_namePL}, ${date_day} ${month_namePL} ${date_year}`  
    }

    loadAmountBalance(){
        let balance_num = totalAmount.children[0].querySelector("span");
        console.log(balance_num)
        balance_num.textContent = this.loggedUserData["ACC_BALANSE"]
    }


    async askForHistory(){

        const data = {
          acc_id: this.loggedUserData["ID"],
          };
  
        const jsonData = JSON.stringify(data);
        let requestOptions = {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json' 
            },
            redirect: 'follow',
            body: jsonData,
            
          };
    
        const request_connect = await fetch("http://127.0.0.1:5000/transfers/last_history", requestOptions);
        if (request_connect.ok) {
          let response = await request_connect.json()
        //   console.log(response)
          return response
        }
    }


    async takeDefoult_transactions(){

        let requestOptions = {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json' 
            },
            redirect: 'follow',
            
          };
    
        const request_connect = await fetch("http://127.0.0.1:5000/transfers/defoult", requestOptions);
        if (request_connect.ok) {
          let response = await request_connect.json()
          return response
        }
    }

    checkTransferTitle(){
        if (TransferTitle.value == ""){
            return "Przelew środków"
        }
        else{
            return TransferTitle.value
        }
    }



    async MakeNewTransfer(){
        const data = {
            from_acc: this.loggedUserData["ACC_NUM"],
            to_acc: TransferAccNumber.value,
            amount: Number(TransferAmount.value),
            date: TransferDate.value,
            name: this.loggedUserData["NAME"],
            surname: this.loggedUserData["L_NAME"],
            title: this.checkTransferTitle(),
            desc: TransferDescription.value
        };

        console.log(data)
        const jsonData = JSON.stringify(data);
        let requestOptions = {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json' 
            },
            redirect: 'follow',
            body: jsonData,
            
        };
    
        const request_connect = await fetch("http://127.0.0.1:5000/transfers/newtransfer", requestOptions);
        if (request_connect.ok) {
            let response = await request_connect.json()
            return response
        }
    }
    
}

class DashboardInputOperator{
    constructor(user_amount){
        this.AccountNumberChecker();
        this.AvailableAmount(user_amount);
        this.CurrentDate();
    }

    AccountNumberChecker(){

        document.querySelector('#transfer-acc-number').addEventListener('input', function(e) {
            let value_input = this.value.split(" ").join("");

            if (value_input.length > 0) {
                value_input = value_input.match(new RegExp('.{1,4}', 'g')).join(" ");
            }
            this.value = value_input;
        });
    }

    AvailableAmount(user_amount){
        TransferAmount.addEventListener("input", function(e){
            let input_amount = Number(this.value);
            if (input_amount > user_amount["ACC_BALANSE"]){
                this.value = user_amount["ACC_BALANSE"]

            }
            else if (/\d+\.\d+/.test(input_amount)){
                this.value = input_amount.toFixed(2);
            }
        })
    }

    CurrentDate(){
        let date = new Date();
        let date_day = date.getDate();
        let date_month = date.getMonth() + 1;
        let date_year = date.getFullYear();
        if (date_day < 10){
            date_day = `0${date_day}`
        }
        if (date_month < 10){
            date_month = `0${date_month}`
        }
        TransferDate.value = `${date_year}-${date_month}-${date_day}`
        TransferDate.addEventListener("input", function(e){
            TransferDate.min = `${date_year}-0${date_month}-0${date_day}`
            TransferDate.value = `${date_year}-0${date_month}-0${date_day}`
        })
    }

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



}

class DashboardCreator extends HTMLconstructor {
    constructor(){
        super();
        this.DashboardPage = new DashboardPage();
        if (this.DashboardPage.setupConstruct()["STATUS"]){
            this.prepareDashboard();
        } else{
            console.log("ERROR")
        }
        this.DashboardInputOperator = new DashboardInputOperator(this.DashboardPage.loggedUserData);
    }


    async loadAmount(){
        this.DashboardPage.loadAmountBalance();
        const transaction_history = await this.DashboardPage.askForHistory()
        if (transaction_history["STATUS"]){
            console.log(transaction_history)
            this.create_elements(transaction_history["DATA"])
        }
        else{
            this.defoult_transactions(3);
        }
    }
    async prepareDashboard(){
        await this.DashboardPage.takeDataToLocalStorage();

        this.DashboardPage.loadProfileInfo();
        this.DashboardPage.getDayName();
        await this.loadAmount();
    }

    async defoult_transactions(iterations){
        for (let j of Array(iterations).keys()){
            const def_transactions = await this.DashboardPage.takeDefoult_transactions();
            // console.log(def_transactions)
            // console.log(def_transactions["DATA"]["transfers"][j])
            let create_element = this.createNewDealsCard(
                `${def_transactions["DATA"]["transfers"][j]["NAME"]} ${def_transactions["DATA"]["transfers"][j]["L_NAME"]}`,
                `${def_transactions["DATA"]["transfers"][j]["AMOUNT"]}`)
            lastTransactionContainer.appendChild(create_element)
        }
    }


    
    async create_elements(last_transactions_dict){  
        console.log(last_transactions_dict["transfers"]);
        this.deleteNewDealsCard();
        for (let i of Array(last_transactions_dict["transfers"].length).keys()){
            let create_element = this.createNewDealsCard(
                `${last_transactions_dict["transfers"][i]["NAME"]} ${last_transactions_dict["transfers"][i]["L_NAME"]}`,
                `${last_transactions_dict["transfers"][i]["AMOUNT"]}`)
            lastTransactionContainer.appendChild(create_element)
        }
        if (last_transactions_dict["transfers"].length > 0){
            this.defoult_transactions(3 - last_transactions_dict["transfers"].length)
        }

    }

    closeTransferPopup(){
        TransferContainer.classList.remove("active");
        DashboardMainPage.classList.add("active");
        NavCreateTransfer.classList.remove("active");
        NavDashboardPage.classList.add("active");
    }

    TransferPopupActive(){
        TransferContainer.classList.add("active");
        DashboardMainPage.classList.remove("active");
        NavCreateTransfer.classList.add("active");
        NavDashboardPage.classList.remove("active");
    }


    async checkTransferData(){
        this.DashboardInputOperator.checkForm([TransferAccNumber,TransferAmount,TransferDate]);
        this.DashboardInputOperator.checkLength(TransferAccNumber,16)
        if (this.DashboardInputOperator.checkError()){
            const makeTransfer = await this.DashboardPage.MakeNewTransfer();
            if (makeTransfer["STATUS"]){
                this.closeTransferPopup();
                await this.loadAmount();
            }
        }
    }
    

}
const dashboard = new DashboardCreator()


TransferCloseBtn.addEventListener("click", ()=>{
    dashboard.closeTransferPopup();
})

sendTransferBtn.addEventListener("click", e=>{
    e.preventDefault();
    dashboard.checkTransferData();
})

NavCreateTransfer.addEventListener("click", ()=>{
    dashboard.TransferPopupActive();
})

NavDashboardPage.addEventListener("click", ()=>{
    dashboard.closeTransferPopup();
})