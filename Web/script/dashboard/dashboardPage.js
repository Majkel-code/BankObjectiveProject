const DashboardMainPage = document.querySelector(".main-dashboard");
const profileInfo = document.querySelector(".profile-main>.profile-info");
const totalAmount = document.querySelector(".total-amount");
// const creditAmount = document.querySelector(".total-amount.credit-amount")
const creditAmount = document.querySelector(".total-amount.credit-amount");
const lastTransactionContainer = document.querySelector(".new-deals-cards_list");

// nav buttons
const NavDashboardPage = document.querySelector(".dashboard-page");
const NavCardsMenagment = document.querySelector(".card-mamagment");
const NavCreateTransfer = document.querySelector(".make-new-transfer");


// TRANSFER SECTION QUERY SELECTOR
const TransferContainer = document.querySelector(".new-transfer");
const TransferCloseBtn = document.querySelector(".dashboard-transfer-close-btn");
const TransferAccNumber = document.querySelector("#transfer-acc-number");
const TransferTitle = document.querySelector("#transfer-title");
const TransferAmount = document.querySelector("#transfer-amount");
const TransferDescription = document.querySelector("#transfer-description");
const TransferDate = document.querySelector("#transfer-date");
const TransferCompanyName = document.querySelector("#transfer-company-name");

const sendTransferBtn = document.querySelector("#send-transfer");

const CardsContainer = document.querySelector(".popup-card-managment");
const CardsCloseBtn = document.querySelector(".dashboard-cards-close-btn");
const CardsCreateNewCard = document.querySelector(".addDiv");
const CardsContentDiv = document.querySelector(".popup-card-managment-content");

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

    async userRefreshLogin(){

        const data = {
          acc_id: this.loggedUserData["ID"],
          password: this.loggedUserData["PASSWORD"],
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
          let response = await request_connect.json();
          console.log(response)
          this.dataToLoad = response["DATA"];
          this.saveData();
          this.loadLocalStorage();
        }
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

    async loadCreditBalance(){
        const credit_data = await this.checkCredits();
        console.log(credit_data)
        if (credit_data["STATUS"]){
            let credit_num = creditAmount.querySelector("h3>span");
            console.log(credit_data["DATA"]["credits"][0]["CREDIT_AMOUNT"])
            credit_num.textContent = credit_data["DATA"]["credits"][0]["CREDIT_AMOUNT"]

            let credit_num_monthly = creditAmount.querySelector("h4>span");
            credit_num_monthly.textContent = credit_data["DATA"]["credits"][0]["CREDIT_MONTHLY"]

            let end_date = creditAmount.querySelector("div > p:last-of-type");
            end_date.textContent = credit_data["DATA"]["credits"][0]["END_DATE"]
        }
    }

    async checkCredits(){
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
      
          const request_connect = await fetch("http://127.0.0.1:5000/credit/havecredit", requestOptions);
        if (request_connect.ok) {
            let response = await request_connect.json()
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

    TakeTime(){
        function addZero(i) {
            if (i < 10) {i = "0" + i}
            return i;
        }     
        const d = new Date();
        let h = addZero(d.getHours());
        let m = addZero(d.getMinutes());
        let s = addZero(d.getSeconds());
        let time = h + ":" + m + ":" + s;
        return time
    }



    async MakeNewTransfer(){
        const data = {
            from_acc: this.loggedUserData["ACC_NUM"],
            to_acc: TransferAccNumber.value,
            amount: Number(TransferAmount.value),
            date: TransferDate.value,
            time: this.TakeTime(),
            sender: `${this.loggedUserData["NAME"]} ${this.loggedUserData["L_NAME"]}`,
            company: TransferCompanyName.value,
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
            console.log(response)
            return response
        }
    }

    async AskForCreditCost(){
        let requestOptions = {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json' 
            },
            redirect: 'follow',
            // body: jsonData,
            
        };
        const request_connect = await fetch("http://127.0.0.1:5000/credit/costs", requestOptions);
        if (request_connect.ok) {
            let response = await request_connect.json()
            return response
        }
    }

    async SendCreditForm(requestedAmount, monthLong){
        const data = {
            id: this.loggedUserData["ID"],
            credit: requestedAmount,
            months: monthLong,
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
    
        const request_connect = await fetch("http://127.0.0.1:5000/credit/new", requestOptions);
        if (request_connect.ok) {
            let response = await request_connect.json()
            console.log(response)
            return response
        }
    }
    
}

class DashboardInputOperator{
    constructor(user_amount){
        this.loggedUserData = user_amount
        console.log(user_amount)
        console.log(this.loggedUserData)
        this.AccountNumberChecker();
        this.AvailableAmount(this.loggedUserData);
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
        let input_amount 
        TransferAmount.addEventListener("input", function(e){
            input_amount = Number(this.value);
            console.log(input_amount)
            console.log(user_amount["ACC_BALANSE"])
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
        if (input.value == this.loggedUserData["ACC_NUM"]){
            this.showError(input, `Nieprawidłowy numer konta`);
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
        this.DashboardInputOperator = new DashboardInputOperator(this.DashboardPage.loggedUserData)


    }
    startDashboardOperator(){
        this.DashboardInputOperator = new DashboardInputOperator(this.DashboardPage.loggedUserData)
    }

    async refreshLocalStorages(){
        await this.DashboardPage.userRefreshLogin();
        this.startDashboardOperator()
    }

    async loadAmount(){
        this.DashboardPage.loadAmountBalance();
        await this.DashboardPage.loadCreditBalance();
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
            if (last_transactions_dict["transfers"][i]["AMOUNT"] > 0){
                let create_element = this.createNewDealsCard(
                    `${last_transactions_dict["transfers"][i]["SENDER"]}`,
                    `${last_transactions_dict["transfers"][i]["AMOUNT"]}`)
                    lastTransactionContainer.appendChild(create_element)
                
            }
            else if (last_transactions_dict["transfers"][i]["AMOUNT"] < 0){
                let create_element = this.createNewDealsCard(
                    `${last_transactions_dict["transfers"][i]["SENDER"]}`,
                    `${last_transactions_dict["transfers"][i]["AMOUNT"]}`)
                    lastTransactionContainer.appendChild(create_element)
                
            }
            
        }
        if (last_transactions_dict["transfers"].length > 0){
            this.defoult_transactions(3 - last_transactions_dict["transfers"].length)
        }

    }

    closePopups(){
        [TransferContainer, CardsContainer, CreditContainer].forEach((container)=> container.classList.remove("active"));
        [NavDashboardPage, NavCreateTransfer, NavCardsMenagment].forEach((btn)=> btn.classList.remove("active"))
        DashboardMainPage.classList.add("active");
        NavDashboardPage.classList.add("active");
    }

    openPopup(popup, navBtn = null){
        [DashboardMainPage, TransferContainer, CardsContainer, CreditContainer].forEach((container)=> container.classList.remove("active"))
        popup.classList.add("active");
        if (navBtn != null){
            [NavDashboardPage, NavCreateTransfer, NavCardsMenagment].forEach((btn)=> btn.classList.remove("active"))
            navBtn.classList.add("active");
        }
    }


    async checkTransferData(){
        this.DashboardInputOperator.checkForm([TransferAccNumber,TransferAmount,TransferDate]);
        this.DashboardInputOperator.checkLength(TransferAccNumber,16)
        if (this.DashboardInputOperator.checkError()){
            const makeTransfer = await this.DashboardPage.MakeNewTransfer();
            if (makeTransfer["STATUS"]){
                await this.refreshLocalStorages()
                this.DashboardPage.loggedUserData["ACC_BALANSE"] = makeTransfer["DATA"];
                this.closePopups();
                await this.loadAmount();
            }
        }
    }

    async askCredit(CreditPopup){
        const credit_costs = await this.DashboardPage.AskForCreditCost();
        if (credit_costs["STATUS"]){
            const creditEvery_p = CreditPopup.querySelectorAll(".form-box>p");
            const RRSOelement = creditEvery_p[2];
            RRSOelement.textContent = credit_costs["DATA"]["RRSO"];

            const AdditionalCostelement = creditEvery_p[3]
            AdditionalCostelement.textContent = credit_costs["DATA"]["OTHER_COSTS"];

            let RRSOspan = document.createElement("span");
            RRSOspan.textContent = "%";
            let AdditionalCostspan = document.createElement("span");
            AdditionalCostspan.textContent = "%";

            RRSOelement.appendChild(RRSOspan);
            AdditionalCostelement.appendChild(AdditionalCostspan);
        }
    }

    fill_data_credit(CreditPopup){
        const creditEvery_p = CreditPopup.querySelectorAll(".form-box>p")
        console.log(creditEvery_p[2]);
        creditEvery_p[0].textContent = `${this.DashboardPage.loggedUserData["NAME"]} ${this.DashboardPage.loggedUserData["L_NAME"]}`;
        creditEvery_p[1].textContent = `${this.DashboardPage.loggedUserData["PESEL"]}`;
    }

    calculateCredit(CreditPopup){
        const creditEvery_p = CreditPopup.querySelectorAll(".form-box>p")

        const RRSOelement = creditEvery_p[2].textContent
        let RRSO_value = Number(RRSOelement.split("%")[0])
        let month_RRSO_value = RRSO_value / 12 / 100
        
        const AdditionalCostelement = creditEvery_p[3].textContent
        let AdditionalConst_value = Number(AdditionalCostelement.split("%")[0])*0.01

        const AmountValueElement = CreditPopup.querySelector("#span-amountValue");
        let AmountValue = Number(AmountValueElement.textContent);
        const MonthValueElement = CreditPopup.querySelector("#span-monthValue");
        let MonthValue = Number(MonthValueElement.textContent);
        const resultAmountElement = creditEvery_p[4];
        const resultMonthAmount = creditEvery_p[5];
        if (AmountValue > 0 && MonthValue > 0){

            let monthly_payment = AmountValue * (month_RRSO_value * (1 + month_RRSO_value)**MonthValue) / ((1+month_RRSO_value)**MonthValue-1)

            let total_interest = monthly_payment * MonthValue - AmountValue

            let actual_apr = (total_interest / AmountValue) / (MonthValue / 12) * 100

            let total_repayment = AmountValue + total_interest

            resultAmountElement.textContent = total_repayment.toFixed(2)
            let resultSpan = document.createElement("span")
            resultSpan.innerText = "zl"
            resultAmountElement.appendChild(resultSpan)

            resultMonthAmount.textContent = monthly_payment.toFixed(2)
            let resultSpanMonth = document.createElement("span")
            resultSpanMonth.innerText = "zl"
            resultMonthAmount.appendChild(resultSpanMonth)
        }
    }

    CreditForm(CreditPopup){
        const creditEvery_p = CreditPopup.querySelectorAll(".form-box>p")
        // const resultAmountElement = creditEvery_p[4].textContent;
        // const resultAmountNumber = Number(resultAmountElement.split("zl")[0]);
        const MonthValueElement = CreditPopup.querySelector("#span-monthValue");
        let MonthValue = Number(MonthValueElement.textContent);
        const AmountValueElement = CreditPopup.querySelector("#span-amountValue");
        let AmountValue = Number(AmountValueElement.textContent);
        // console.log(resultAmountNumber);
        if (AmountValue > 0 && MonthValue > 0){
            this.DashboardPage.SendCreditForm(AmountValue, MonthValue);

        }
    }


}
const dashboard = new DashboardCreator()

CardsCreateNewCard.addEventListener("click", e=>{
    e.preventDefault(); 
    dashboard.AddNewCard();
})

TransferCloseBtn.addEventListener("click", ()=>{
    dashboard.closePopups();
})
CardsCloseBtn.addEventListener("click", ()=>{
    dashboard.closePopups();
})

sendTransferBtn.addEventListener("click", e=>{
    e.preventDefault();
    dashboard.checkTransferData();
})

NavCreateTransfer.addEventListener("click", ()=>{
    dashboard.openPopup(TransferContainer, NavCreateTransfer);
})

NavDashboardPage.addEventListener("click", ()=>{
    dashboard.openPopup(DashboardMainPage, NavDashboardPage);
})
NavCardsMenagment.addEventListener("click", ()=>{
    dashboard.openPopup(CardsContainer,NavCardsMenagment);
})

const openCreditPopupBtn = document.querySelector(".open-credit-popup");
const CreditContainer = document.querySelector(".credit-popup");
const CreditCloseBtn = document.querySelector(".dashboard-credit-close-btn");
const SendCreditFormBtn = document.querySelector("#take-credit-btn");

openCreditPopupBtn.addEventListener("click", ()=>{
    dashboard.askCredit(CreditContainer)
    dashboard.openPopup(CreditContainer);
    dashboard.fill_data_credit(CreditContainer)
})
CreditCloseBtn.addEventListener("click", ()=>{
    dashboard.closePopups()
})

// CREDIT SLIDERS
const sliderMonth = document.getElementById("input-monthRange");
const outputMonth = document.getElementById("span-monthValue");
const sliderAmonunt = document.getElementById("input-amountRange");
const outputAmount = document.getElementById("span-amountValue");

sliderMonth.oninput = function() {
    outputMonth.innerHTML = this.value;
    dashboard.calculateCredit(CreditContainer);
}


sliderAmonunt.oninput = function() {
    outputAmount.innerHTML = this.value;
    dashboard.calculateCredit(CreditContainer);
}


SendCreditFormBtn.addEventListener("click", ()=>{
    dashboard.CreditForm(CreditContainer);
})