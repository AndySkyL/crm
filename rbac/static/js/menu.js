
    $('.multi-menu .title').click(function () {
        if (!$(this).next().hasClass('hide')){
            $(this).next().addClass('hide')
        }else {
            $(this).next().removeClass('hide')
            $(this).parent().siblings().find('.body').addClass('hide')
        }

    })
