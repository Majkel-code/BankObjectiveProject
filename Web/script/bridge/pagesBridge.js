class MultiPageBridge{
    constructor(){
        this.dataToLoad = null;
        this.logout = false;
        
    }
    saveData(){
        localStorage.myData = JSON.stringify(this.dataToLoad);
    }

    // sessionEnd(){
    //     this.logout = true
    //     localStorage.logout = this.logout
    // }

}