class MultiPageBridge{
    constructor(){
        this.dataToLoad = null;
        
    }
    saveData(){
        localStorage.myData = JSON.stringify(this.dataToLoad);
    }

}