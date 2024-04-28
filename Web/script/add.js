var addedDivs = 0; // Inicjalizacja licznika dodanych elementów

document.getElementById('addDiv').addEventListener('click', function(event) {
    event.preventDefault(); 

    if (addedDivs < 2) { // Sprawdzanie, czy nie przekroczono limitu
        var newDiv = document.createElement('div'); // Tworzenie nowego elementu div
        newDiv.className = 'credit mc'; // Dodanie klasy do nowego diva


        var innerDiv = document.createElement('div'); // Tworzenie nowego elementu div dla zawartości
        innerDiv.className = 'content-container'; // Dodanie klasy do nowego diva zawartości

        var img = document.createElement('img'); // Tworzenie nowego elementu img
        img.src = 'https://res.cloudinary.com/dzavwgc6d/image/upload/v1463341473/Middle_vsnsoj.png'; // Ustawienie źródła obrazu


        var h2 = document.createElement('h2'); // Tworzenie nowego elementu h2
        h2.textContent = '**** **** **** 2562'; // Ustawienie tekstu w h2


        var p = document.createElement('p'); // Tworzenie nowego elementu p
        p.textContent = 'Valid Thru: 12/26'; // Ustawienie tekstu w p

       
        innerDiv.appendChild(img); // Dodanie obrazu do diva zawartości
        innerDiv.appendChild(h2); // Dodanie h2 do diva zawartości
        innerDiv.appendChild(p); // Dodanie p do diva zawartości

        newDiv.appendChild(innerDiv); // Dodanie diva zawartości do nowego diva

        var lastCard = document.querySelector('.credit:last-child'); // Znalezienie ostatniego diva z klasą 'credit'
        if (lastCard) {
            lastCard.parentNode.insertBefore(newDiv, lastCard.nextSibling); // Wstawienie nowego diva przed ostatnim divem
        } else {
            document.body.appendChild(newDiv); // Jeśli nie ma żadnych divów z klasą 'credit', dodajemy nowy div do ciała dokumentu
        }

        addedDivs++; // Zwiększenie licznika dodanych divów
    } else {
        alert("Nie można mieć wiecej kart płatniczych!"); // Wyświetlenie alertu, gdy przekroczono limit
    }
});
