(function () {
    select_variation = document.getElementById('select-variation');
    price_variation = document.getElementById('price-variation');
    promotional_price_variation = document.getElementById('promotional-price-variation');

    if(!select_variation){
        return;
    }

    if(!price_variation){
        return;
    }

    select_variation.addEventListener('change', function(){
        price = this.options[this.selectedIndex].getAttribute('price-data');
        promotional_price = this.options[this.selectedIndex].getAttribute('promotional-price-data');

        price_variation.innerHTML = price;

        if(promotional_price_variation){
            promotional_price_variation.innerHTML = promotional_price;
        }
    })
})();

document.addEventListener('DOMContentLoaded', function(){
    var productList = document.querySelector('.products');
    var productItems = productList.querySelectorAll('.product-card');
    var productCount = productItems.length;

    if(productCount > 3){
        model = document.querySelector('.section-products')
        model.classList.add('more-products')
    } else {
        model.classList.remove('more-products')
    }
})