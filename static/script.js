// script.js
function showQuantitySelector(productId) {
    var selector = document.getElementById(productId);
    selector.style.display = 'block';
}

function changeQuantity(productId, change) {
    var quantityInput = document.getElementById('quantity_' + productId);
    var currentQuantity = parseInt(quantityInput.value);
    var newQuantity = currentQuantity + change;
    if (newQuantity > 0) {
        quantityInput.value = newQuantity;
    }
}

function updateCartQuantity(productId) {
    var quantity = document.getElementById('quantity-' + productId).value;
    var updateUrl = '/update_cart/' + productId + '?quantity=' + quantity;
    window.location.href = updateUrl;
}


function updateDeliveryMethod() {
    var deliveryMethod = document.querySelector('input[name="delivery"]:checked').value;
    document.getElementById('addressField').style.display = deliveryMethod == '宅配到府' ? 'block' : 'none';
    document.getElementById('storeField').style.display = deliveryMethod == '超商取貨' ? 'block' : 'none';
    document.getElementById('marketField').style.display = deliveryMethod == '市場自取' ? 'block' : 'none';
}
