$(document).ready(function(){

  /*Функция проверки наличия элемента на странице*/
  $.fn.exists = function() {
        return $(this).length;
    }
    /*функция проверки атрибута у элемента*/
  $.fn.hasAttr = function(name) {
    return this.attr(name) !== undefined;
  };

  /*Логика табов*/
  if($("ul.tab_menu").exists()) {
    $('ul.tab_menu').on('click', 'li:not(.active)', function() {
      $(this).addClass('active').siblings().removeClass('active');
      $('.tabs').find('div.tab_content').removeClass('active').eq($(this).index()).addClass('active');
    });
  }

  /*Ползунок цены в фильтре*/
  if($("#price").exists()) {
    var startSlider = $('#price')[0],
      minInput = $('#min-price')[0],
      maxInput = $('#max-price')[0],
      min_start = $('#min-price').data('price-min'),
      min_start = $('#max-price').data('price-max');
    noUiSlider.create(startSlider, {
        start: [0, 3000],
        step: 10,
        range: {
            'min': [5],
            'max': [3000]
        },
      format: {
        to: function (value) {
          return parseInt(value);
        },
        from: function (value) {
          return Number(value);
        }
      }
    });
    startSlider.noUiSlider.on('update', function (values, handle) {
        var value = values[handle];
        if (handle) {
            maxInput.value = value;
        } else {
            minInput.value = value;
        }
    });
    minInput.addEventListener('change', function () {
        startSlider.noUiSlider.set([this.value, null]);
    });
    maxInput.addEventListener('change', function () {
        startSlider.noUiSlider.set([null, this.value]);
    });
  }

  /*Кнопки мобильной навигации*/
  $("div").click(function(){
    if($(this).hasAttr('data-popup-button')){
      var popup_name = $(this).attr('data-popup-button'),
        selector = $("div[data-popup = " + popup_name + "]");
      selector.addClass("active_popup");
      if(selector.find("input[type=text]").length > 0){
        selector.find("input[type=text]").focus();
      }
    }
  });
  $(".close_popup_button").click(function(){
    var active_popup_name = $(this).parents("div[data-popup]").attr('data-popup');
    $("div[data-popup=" + active_popup_name + "]").removeClass("active_popup");
  });

  /*Настройка слайда на главной странице*/
  if($(".slide-container").exists()) {
    var swiper = new Swiper('.slide-container', {
      autoplay: {
            delay: 3000,
            disableOnInteraction: false,
          },
        navigation: {
          nextEl: '.slide-next',
          prevEl: '.slide-prev',
      },
      });
  }

  /*Форма выборы оплаты + валидация e-mail*/
  $(".payment").click(function(){
    if($(this).hasAttr('data-price')){
      var price = parseFloat($(this).attr('data-price'));
      $(".final_coast span").html(price);
    }
  });
    function isValidEmailAddress(emailAddress) {
    var pattern = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);
    return pattern.test(emailAddress);
    };
  $('#payment').submit(function(){
        var email = $('.mail input[name=mail]').val();
        var status_mail = isValidEmailAddress(email);
        var status_check = $("#payment input[type=radio]:checked").exists();
        $("#payment_error").empty();
        if ((status_mail == false)||(status_check==0)){
          if(status_mail == false){
            if(!$("div[data-error=mail_error_message]").exists()) {
              $("#payment_error").append("<div data-error='mail_error_message'>Некорректно заполнено поле E-mail</div>");
            }
            console.log("ошибка в mail");
          }
          if(status_check==0){
            if(!$("div[data-error=payment_error_message]").exists()) {
              $("#payment_error").append("<div data-error='payment_error_message'>Вы не выбрали способ оплаты</div>");
            }
            console.log("не указан способ оплаты");
          }
        }else{
          console.log("отправлять");
        }
        return false;
    });


    /*Табы на главной странице*/
    $("div.tab_item").click(function() {
      /*
      $("div.tab_item").removeClass("active_tab");
      $(this).addClass("active_tab");
      */
      var elem = $(this).nextAll("div.tab_block:first");
      if (elem.is(":hidden")) {
        if($(document).width()>500){
          $("div.tab_block:visible").removeClass("active");
        }
        elem.addClass("active");
      }else{
        if($(document).width()<500){
          elem.removeClass("active");
        }
      }
    });


});