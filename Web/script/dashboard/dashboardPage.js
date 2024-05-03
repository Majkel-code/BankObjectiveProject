class DashboardPage  {
    constructor(){
         this.loggedUserData = JSON.parse(localStorage.myData)
        console.log(this.loggedUserData)
    }

}
const dashboard = new DashboardPage()
