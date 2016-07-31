function sendPost(form) {
    var msg = $(form).serialize();
    //отправляю POST запрос и получаю ответ
    $.ajax({
        type:'post',//тип запроса: get,post либо head
        url:'set_comment.html',//url адрес файла обработчика
        data:msg,//параметры запроса
        response:'text',//тип возвращаемого ответа text либо xml
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

