document.addEventListener("DOMContentLoaded", function() {
    // Find all filter buttons
    var filterButtons = document.querySelectorAll(".filter-button");

    // Attach click event listener to each filter button
    filterButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            var category = this.dataset.category; // Get the category from the button's data attribute

            // Send AJAX request to the server
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/filter");
            xhr.setRequestHeader("Content-Type", "application/json");

            xhr.onreadystatechange = function() {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        var matchingProducts = JSON.parse(xhr.responseText);
                        updateProductList(matchingProducts);
                    } else {
                        // Handle errors
                    }
                }
            };

            var data = JSON.stringify({ category: category }); // Prepare the data to send
            xhr.send(data); // Send the request
        });
    });
    
// Function to update the product list with matching products
function updateProductList(matchingProducts) {
    var imageGrid = document.querySelector(".image-grid");
    imageGrid.innerHTML = ""; // Clear the existing product list

    // Iterate over the matching products and add them to the product list
    matchingProducts.forEach(function(product) {
        var productLink = document.createElement("a");
        productLink.href = "/product/" + product.product_id;

        var productImage = document.createElement("img");
        productImage.src = product.image_url;
        productImage.alt = "Image";

        productLink.appendChild(productImage);
        imageGrid.appendChild(productLink);
    });
}
});


function showCardDetails() {
    document.getElementById('cardDetails').style.display = "block";
    document.getElementById('notAvailable').style.display = "none";
    document.getElementById("paymentSuccess").style.display = "none";
}

function showPopup(id) {
    document.getElementById('cardDetails').style.display = "none";
    document.getElementById("paymentSuccess").style.display = "none";
    var popup = document.getElementById('notAvailable');
    popup.style.display = "flex";
    popup.style.alignItems = "center";
    popup.style.justifyContent = "center";
}

function showPaymentSuccess(id) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/check_payment');
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            document.getElementById('cardDetails').style.display = "none";
            document.getElementById('notAvailable').style.display = "none";
            if (response.success) {
                var popup = document.getElementById("paymentSuccess");
                popup.style.display = "flex";
                popup.style.alignItems = "center";
                popup.style.justifyContent = "center";
            } else {
                var popup = document.getElementById("paymentFail");
                popup.style.display = "flex";
                popup.style.alignItems = "center";
                popup.style.justifyContent = "center";
            }
        }
    };

    var cardNumber = document.querySelector('.card-number').value;
    var cvv = document.querySelector('.cvv').value;
    var expiry = document.querySelector('.card-expiry').value;
    var email = document.querySelector('input[type="email"]').value;

    var validationPassed = true; // Flag to track overall validation result

    if (!validateCardNumber(cardNumber)) {
        var cardNumberMessage = document.getElementById('cardNumberMessage');
        cardNumberMessage.textContent = 'Invalid card number.';
        cardNumberMessage.classList.remove('success');
        cardNumberMessage.classList.add('error');
        validationPassed = false;
    }

    if (!validateExpiry(expiry)) {
        var expiryMessage = document.getElementById('expiryMessage');
        expiryMessage.textContent = 'Invalid expiry date.';
        expiryMessage.classList.remove('success');
        expiryMessage.classList.add('error');
        validationPassed = false;
    }

    if (!validateEmail(email)) {
        var emailMessage = document.getElementById('emailMessage');
        emailMessage.textContent = 'Invalid email address.';
        emailMessage.classList.remove('success');
        emailMessage.classList.add('error');
        validationPassed = false;
    }

    if (!validateCVV(cvv)) {
        var cvvMessage = document.getElementById('cvvMessage');
        cvvMessage.textContent = 'Invalid CVV.';
        cvvMessage.classList.remove('success');
        cvvMessage.classList.add('error');
        validationPassed = false;
    }

    if (!validationPassed) {
        return; // Exit early if validation failed
    }

    xhr.send(
        JSON.stringify({
            product_id: "{{ product['product_id'] }}",
            card_number: cardNumber,
            cvv: cvv,
            expiry: expiry,
            amount: "{{ product['price'] }}",
            email: email
        })
    );
}


function validateCardNumber(cardNumber) {
    // Remove all non-digit characters from the card number
    cardNumber = cardNumber.replace(/\D/g, '');

    // Check if the card number is a valid Visa, Mastercard, or Verve number
    return /^4[0-9]{12}(?:[0-9]{3})?$/.test(cardNumber) || // Visa
        /^(5[1-5]|2[2-7])[0-9]{14}$/.test(cardNumber) || // Mastercard
        /^5061[0-9]{15}$/.test(cardNumber); // Verve
}

function validateExpiry(expiry) {
    // Check if the expiry is in the format MM/YY
    if (/^(0[1-9]|1[0-2])\/[0-9]{2}$/.test(expiry)) {
        // Extract the month and year from the expiry
        var parts = expiry.split('/');
        var month = parseInt(parts[0]);
        var year = parseInt(parts[1]);

        // Get the current date
        var currentDate = new Date();
        var currentYear = currentDate.getFullYear() % 100; // Get the last two digits of the current year
        var currentMonth = currentDate.getMonth() + 1; // Months are zero-based, so add 1

        // Check if the expiry is a future date
        if (year > currentYear || (year === currentYear && month >= currentMonth)) {
            return true;
        }
    }
    return false;
}

function validateCVV(cvv) {
    // Check if the CVV is exactly 3 digits
    return /^\d{3}$/.test(cvv);
}


function validateEmail(email) {
    // Check if the email address is valid
    var emailRegex = /^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$/i;

    return emailRegex.test(email);
}


function validateCardNumberInput() {
    var cardNumber = cardNumberInput.value;

    if (validateCardNumber(cardNumber)) {
        cardNumberMessage.textContent = 'Card number is valid.';
        cardNumberMessage.classList.remove('error');
        cardNumberMessage.classList.add('success');
    } else {
        cardNumberMessage.textContent = 'Invalid card number.';
        cardNumberMessage.classList.remove('success');
        cardNumberMessage.classList.add('error');
    }
}

function validateExpiryInput() {
    var expiry = expiryInput.value;

    if (validateExpiry(expiry)) {
        expiryMessage.textContent = 'Expiry date is valid.';
        expiryMessage.classList.remove('error');
        expiryMessage.classList.add('success');
    } else {
        expiryMessage.textContent = 'Invalid expiry date.';
        expiryMessage.classList.remove('success');
        expiryMessage.classList.add('error');
    }
}

function validateEmailInput() {
    var email = emailInput.value;

    if (validateEmail(email)) {
        emailMessage.textContent = 'Email address is valid.';
        emailMessage.classList.remove('error');
        emailMessage.classList.add('success');
    } else {
        emailMessage.textContent = 'Invalid email address.';
        emailMessage.classList.remove('success');
        emailMessage.classList.add('error');
    }
}

function validateCVVInput() {
    var cvv = cvvInput.value;

    if (validateCVV(cvv)) {
        cvvMessage.textContent = 'CVV is valid.';
        cvvMessage.classList.remove('error');
        cvvMessage.classList.add('success');
    } else {
        cvvMessage.textContent = 'Invalid CVV.';
        cvvMessage.classList.remove('success');
        cvvMessage.classList.add('error');
    }
}

