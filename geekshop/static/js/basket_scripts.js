window.onload = function () {
    $('.basket_list').on('keyup', 'input[type="number"]', function () {
        update_basket_list(event.target)
    });
    $('.basket_list').on('click', 'input[type="number"]', function () {
        update_basket_list(event.target)
    });
        function update_basket_list(t_href) {
        $.ajax({
            url: "/basket/edit/" + t_href.name + "/" + t_href.value + "/",
            success: function (data) {
                $('.basket_list').html(data.result);
                console.log('ajax done');
            },
        });
        event.preventDefault();
    }
}
