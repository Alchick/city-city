function sendPost(form) {
    var date = $(form).serialize();
    val = document.getElementById('counter');
    if (val){
        date = date + '&' + 'rating' + '=' + val.value;}
    //отправляю POST запрос и получаю ответ
    $.ajax({
        type:'post',//тип запроса: get,post либо head
        url:'set_comment.html',//url адрес файла обработчика
        data:date,//параметры запроса
        v:val,
        response:'success',//тип возвращаемого ответа text либо xml
        success:function(data,v){//возвращаемый результат от сервера
            if (val){
                alert(val);
                var message = JSON.parse(JSON.stringify(data));
                $('#result').html(message['message_words']);
              }
            else {
              Data = new Date();
              var new_comment = "<p>Имя пользователя - " + $("input[name=name]").val()+ "</p>"+
                                "<p>Дата добавления - " + moment(Data).fromNow() + "</p>" +
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

function time_format(){
    data = $('.time-handle').html();
    $('.time-handle').html(moment(data).format('YYYY-MM-DD HH:MM:SS'));
}

function time_format_fromNow(){
    data = $('.time-handle').html();
    $('.time-handle').html(moment(data).fromNow());
}

function get_comment(){
    $.ajax({    
    type:'GET',
    url:'get_file.html',
    data:{get_comment:'get_comment'},
    success:function(data){
        alert(typeof(data.a[0]));
        var mydiv = document.getElementById('user_comment');
        for (var i = 0; i <=3; i++){
            var div = document.createElement('div');
            div.innerHTML = "<p><span class='comment_fieldi'>Имя пользователя</span> - " + data.a[i][0] + "</p>" +
            "<p><span class='comment_fieldi'>Комментарий</span> - " + data.a[i][1] + "</p>"+
            "<p><span class='comment_fieldi'>Дата</span> - " + data.a[i][2] + "</p>" + "<br>";
            mydiv.appendChild(div);
        }
    }
   });
}

    
