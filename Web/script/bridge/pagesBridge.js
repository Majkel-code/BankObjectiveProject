class MultiPageBridge {
  constructor() {
    this.dataToLoad = null;
    this.logout = false;
  }
  saveData() {
    localStorage.myData = JSON.stringify(this.dataToLoad);
  }
}
