window.onload = function () {
    let _quantity, _price, orderItemNum, deltaQuantity, orderItemQuantity, deltaCost;
    const quantityArr = [];
    const priceArr = [];

    const TOTAL_FORMS = parseInt($('input[name="order_items-TOTAL_FORMS"]').val());

    let orderTotalQuantity = parseInt($('.order_total_quantity').text()) || 0;
    let orderTotalCost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;

    for (let i = 0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name="order_items-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));

        quantityArr[i] = _quantity;
        if (_price) {
            priceArr[i] = _price;
        } else {
            priceArr[i] = 0;
        }
    }

    if (!orderTotalQuantity) {
        for (let i = 0; i < TOTAL_FORMS; i++) {
            orderTotalQuantity += quantityArr[i];
            orderTotalCost += priceArr[i] * quantityArr[i];
        }
        $('.order_total_quantity').html(orderTotalQuantity.toString());
        $('.order_total_cost').html(orderTotalCost.toFixed(2)).toString();
    }

    $('.order_form').on('click', 'input[type="number"]', function () {
        let target = event.target;
        orderItemNum = parseInt(target.name.replace('order_items-', '').replace('-quantity', ''));
        if (priceArr[orderItemNum]) {
            orderItemQuantity = parseInt(target.value);
            deltaQuantity = orderItemQuantity - quantityArr[orderItemNum];
            quantityArr[orderItemNum] = orderItemQuantity;
            orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity);
        }
    });

    $('.order_form select').change(function () {
        const target = event.target;
        console.log(target);
    });

    function orderSummaryUpdate(orderItemPrice, deltaQuantity) {
        deltaCost = orderItemPrice * deltaQuantity;
        orderTotalCost = Number((orderTotalCost + deltaCost).toFixed(2));
        orderTotalQuantity = orderTotalQuantity + deltaQuantity;
        $('.order_total_quantity').html(orderTotalQuantity.toString());
        $('.order_total_cost').html(orderTotalCost.toFixed(2)).toString();
    }

    function deleteOrderItem(row) {
        const targetName = row[0].querySelector('input[type="number"]').name;
        orderItemNum = parseInt(targetName.replace('order_items-', '').replace('-quantity', ''));
        deltaQuantity = -quantityArr[orderItemNum];
        orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity);
    }

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'order_items',
        removed: deleteOrderItem
    });
}