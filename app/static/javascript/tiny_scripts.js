function sendPost(form) {
    var date = $(form).serialize();
    val = document.getElementById('counter').value;
    if (val){
        date = date + '&' + 'rating' + '=' + val;}
    //отправляю POST запрос и получаю ответ
    $.ajax({
        type:'post',//тип запроса: get,post либо head
        url:'set_comment.html',//url адрес файла обработчика
        data:date,//параметры запроса
        response:'success',//тип возвращаемого ответа text либо xml
        success:function (data) {//возвращаемый результат от сервера
            alert(data);
        }
    });
}


setTimeout(function(){$('.flash-error').fadeOut('fast')}, 5000);


function doClear(element) {
    if (element.value == element.defaultValue) { element.value = "" };
}

function doDefault(element) { 
    if (element.value == "") { element.value = element.defaultValue } 
}


function counterr(id) {
    document.getElementById(id).value=parseInt(document.getElementById(id).value) + 1;
    if (document.getElementById(id).value == 11){
        document.getElementById(id).value = 0;
    }
};

