$(document).ready(function() {

    jQuery.fn.exists = function() {
        return $(this).length;
    }

    /*Плавная анимация до формы*/
    $('.label_button').click(function(){
        var position = ($(".order-mail-box").offset().top) - 50;
        $('html, body').delay(300).animate({scrollTop: position}, 1000);
    });
    
    /*Проверяем валидность формы майла для покупателя*/
    function isValidEmailAddress(emailAddress) {
        var pattern = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);
        return pattern.test(emailAddress);
    }
    $('.order-mail-mail input').focus(function(){
        $('.order-mail-mail input').removeClass("field-error");
    });

    $('.order-form').submit(function(){
        var email = $('.order-mail-mail input').val();
        if(!isValidEmailAddress(email)){
            $('.order-mail-mail input').addClass("field-error");
            return false;
        }
    });

    /*Swiper_slider*/
    if($(".swiper-container").exists()) {
        var mySwiper = new Swiper('.swiper-container', {
            speed: 400,
            spaceBetween: 0,
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            autoplay: {
                delay: 3000,
            },
        });
    }

    /*Анимация бордюра*/
    if($("#border-animation").exists()) {
        $(function(){
            $("#border-animation").liveBorder({
                top: true,
                right: true,
                bottom: true,
                left: true
            });
        });
    }

    /*Показываем / Скрываем сэндвич меню*/
    $(".open-menu").click(function(){
        if($(".top-navigation-container").is(":visible")){
            $(".top-navigation-container").hide();
        }
        else{
            $(".top-navigation-container").show();
        }
        event.preventDefault();
    });


});