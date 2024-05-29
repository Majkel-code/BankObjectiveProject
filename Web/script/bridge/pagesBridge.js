class MultiPageBridge {
  constructor() {
    this.dataToLoad = null;
    this.logout = false;
  }

  /**
   * Saves the data to the local storage.
   */
  saveData() {
    localStorage.myData = JSON.stringify(this.dataToLoad);
  }
}
