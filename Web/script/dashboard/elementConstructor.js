class HTMLconstructor{
    constructor(){

    }

    deleteNewDealsCard(){
        document.querySelectorAll(".new-deals-cards_item").forEach(element => element.remove())
    }

    createNewDealsCard(name, price, imageUrl = "../html/img/c3.png") {
        const cardItem = document.createElement("div");
        cardItem.classList.add("new-deals-cards_item");
      
        // Image section
        const imageContainer = document.createElement("div");
        imageContainer.classList.add("new-deals-cards_item-img");
        const image = document.createElement("img");
        image.src = imageUrl;
        image.alt = "";
        imageContainer.appendChild(image);
      
        // Info section
        const infoContainer = document.createElement("div");
        infoContainer.classList.add("new-deals-cards_item-info");
        const title = document.createElement("h3");
        title.textContent = name;
        const priceText = document.createElement("p");
        priceText.textContent = price + "zl";
        if (price<0){
            priceText.style.color = "#ea0303"
        }
        else{
            priceText.style.color = "#3bba3b"
        }
        infoContainer.appendChild(title);
        infoContainer.appendChild(priceText);
      
        // New badge
        const newBadge = document.createElement("div");
        newBadge.classList.add("new-deals-cards_item-new");
        newBadge.textContent = "New";
      
        // Append all elements
        cardItem.appendChild(imageContainer);
        cardItem.appendChild(infoContainer);
        cardItem.appendChild(newBadge);
        // cardItem.appendChild(iconContainer);
      
        return cardItem;
      }
}