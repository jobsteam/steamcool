$(document).ready(function() {

    /*Читать далее кнопка*/
    $('article').readmore({
        speed: 500,
        maxHeight: 200,
        moreLink: '<a class="readmore" href="#">читать далее...</a>',
        lessLink: '<a class="readmore" href="#">скрыть...</a>'
    });

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
});