//find current url
function shineLinks(id){
  try{
    var el=document.getElementById(id).getElementsByTagName('a');//ищем наш div в <span class="caps">DOM</span>
    var url=document.location.href;//палим текущий урл
    for(var i=0;i<el.length; i++){
      if (url==el[i].href){
        el[i].className = 'active_menu';//если урл==текущий, добавляем класс
        };
      };
    }
  catch(e){}
};

