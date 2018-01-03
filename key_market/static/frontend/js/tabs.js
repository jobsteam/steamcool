$(function () {
    var tabContainers = $('div.tab_menu > div'); // получаем массив контейнеров
    tabContainers.hide().filter(':first').show(); // прячем все, кроме первого
    // далее обрабатывается клик по вкладке
    $('div.tab_menu ul.tabs a').click(function () {
        tabContainers.hide(); // прячем все табы
        tabContainers.filter(this.hash).show(); // показываем содержимое текущего
        $('div.tab_menu ul.tabs a').removeClass('active'); // у всех убираем класс 'selected'
        $(this).addClass('active'); // текушей вкладке добавляем класс 'selected'
        return false;
    }).filter(':first').click();
});