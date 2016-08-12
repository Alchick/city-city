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
        success:function(data,val){//возвращаемый результат от сервера
            if (val){
                var message = JSON.parse(JSON.stringify(data));
                $('#result').html(message['message_words']);
              }
            else {
              Data = new Date();
              var new_comment = "<p>Имя пользователя - " + $("input[name=name]").val()+ "</p>"+
                                "<p>Дата добавления - " + Data + "</p>" +
                                "<p>Комментарий -  " + $("textarea[name=comment]").val()+"</p>";
              $('#new_comment').html(new_comment);
            }
        },
        error:function(){
            message = "<p style=\"color:red\">Произошла ошибка при отправке данных. Попробуйте снова или напишите нам</p>";
            $('#result').html(message);
        }
    });
}


setTimeout(function(){$('.flash-message').fadeOut('fast')}, 5000);


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

function submitForm(obj) {
    obj.form.submit()
    obj.form.reset();
    
    return false;
}
