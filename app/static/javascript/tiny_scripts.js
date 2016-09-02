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

function time_format(data){
    document.write(moment.utc(data).local().format('YYYY-MM-DD HH:mm:ss'));
}

function time_fromNow(data){
    document.write(moment.utc(data).local().fromNow());
}

function add_comment(data, person){
//     var comments = document.getElementById(object_id);
     var comments = document.getElementById(person+'_comments');
     comments.innerHTML = '';
     for (var i = 0; i<data.length; i++){
        var comment = document.createElement('div');
        comment.className = 'comment';
        console.log(data[i][0]);
        comment.innerHTML = "<p><span class='comment_field'>Имя пользователя</span> - " + data[i][0] + "</p>" +
        "<p><span class='comment_field'>Комментарий</span> - " + data[i][2] + "</p>"+
        "<p><span class='comment_field'>Дата добавления</span> - " + moment(data[i][1]).fromNow() + "</p><br>";
        comments.appendChild(comment);
     }
}


function get_comment(article_id, j, person){
    i = i + j;
    var next_page = document.querySelector('#'+person+'_next_button');
    var previous_page = document.querySelector('#'+person+'_previous_button');
    console.log('this is '+ next_page);
    $.ajax({    
    type:'GET',
    url:'get_comment',
    data:{id:article_id,iter:i, person:person},
    success:function(data){
        add_comment(data[person+'_comments'], person);
        if (data[person+'_length'] <= 3){
            next_page.style.display = "none"}

        else{next_page.style.display = "inline"}

        if (i < 2){
            previous_page.style.display = 'none'}
            //document.getElementById('previous_page').style.display = 'none'}
            else{previous_page.style.display = 'inline'};
        
    }
   });
}

    
