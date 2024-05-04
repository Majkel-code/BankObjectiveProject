const profileInfo = document.querySelector(".profile-main>.profile-info");
const totalAmount = document.querySelector(".total-amount");


class DashboardPage extends MultiPageBridge {
    constructor(){
        super();
        // this.sessionEnd();
        this.setupConstruct();
    }

    setupConstruct(){
        let storage = this.loadLocalStorage();
        if (storage["STATUS"]){
            this.prepareDashboard();
        }
        else{
            console.log(storage["ERROR"])
            // window.location.href = 'main.html';
        }
    }

    loadLocalStorage(){
        try {
            this.loggedUserData = JSON.parse(localStorage.myData); 
        } catch (error) {
            return {"STATUS": false, "ERROR": "unable load data!"}
        }
        return {"STATUS": true, "ERROR": null}
    }


    prepareDashboard(){
        this.loadProfileInfo();
        this.getDayName();
        this.loadAmountBalance();
        if (this.askForHistory()["STATUS"]){
            console.log("prepareDashboard function")
            // FILL TRANSFER HISTORY
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
        // return `${day_namePL}, ${date_day} ${month_namePL} ${date_year}`     
    }

    loadAmountBalance(){
        let balance_num = document.createElement("span");
        totalAmount.children[0].appendChild(balance_num);
        balance_num.innerText = this.loggedUserData["ACC_BALANSE"]
    }


    // lastTransactions(){

    // }

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
    
        const request_connect = await fetch("http://127.0.0.1:5000/transfers/history", requestOptions);
        if (request_connect.ok) {
          let response = await request_connect.json()
          console.log(response)
          return response
        }
      }



}
const dashboard = new DashboardPage()
