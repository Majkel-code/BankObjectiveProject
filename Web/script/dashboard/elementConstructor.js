class HTMLconstructor {
  constructor() {
    this.addedDivs = 0;
  }

  deleteNewDealsCard() {
    document
      .querySelectorAll(".new-deals-cards_item")
      .forEach((element) => element.remove());
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
    if (price < 0) {
      priceText.style.color = "#ea0303";
    } else {
      priceText.style.color = "#3bba3b";
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

  AddNewCard() {
    if (this.addedDivs < 2) {
      // Sprawdzanie, czy nie przekroczono limitu
      let newDiv = document.createElement("div"); // Tworzenie nowego elementu div
      newDiv.className = "credit-card"; // Dodanie klasy do nowego diva

      let img = document.createElement("img"); // Tworzenie nowego elementu img
      img.src =
        "https://res.cloudinary.com/dzavwgc6d/image/upload/v1463341473/Middle_vsnsoj.png"; // Ustawienie źródła obrazu

      let h2 = document.createElement("h2"); // Tworzenie nowego elementu h2
      h2.textContent = "**** **** **** 2562"; // Ustawienie tekstu w h2

      let p = document.createElement("p"); // Tworzenie nowego elementu p
      p.textContent = "Valid Thru: 12/26"; // Ustawienie tekstu w p

      newDiv.appendChild(img); // Dodanie obrazu do diva zawartości
      newDiv.appendChild(h2); // Dodanie h2 do diva zawartości
      newDiv.appendChild(p); // Dodanie p do diva zawartości

      let lastCard = document.querySelector(".credit-card:last-child"); // Znalezienie ostatniego diva z klasą 'credit'
      if (lastCard) {
        lastCard.parentNode.insertBefore(newDiv, lastCard.nextSibling); // Wstawienie nowego diva przed ostatnim divem
      } else {
        document.body.appendChild(newDiv); // Jeśli nie ma żadnych divów z klasą 'credit', dodajemy nowy div do ciała dokumentu
      }

      this.addedDivs++; // Zwiększenie licznika dodanych divów
    } else {
      alert("Nie można mieć wiecej kart płatniczych!"); // Wyświetlenie alertu, gdy przekroczono limit
    }
  }
}
