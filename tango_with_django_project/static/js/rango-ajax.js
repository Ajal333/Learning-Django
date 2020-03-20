    $('#likes').click(() => {
        let cat_id;
        cat_id = $(this).attr('data-cat_id');
        $.get('/rango/like/', {category_id = cat_id}, data => {
            $('#like_count').html(data);
            $('#likes').hide();
        })      
    })