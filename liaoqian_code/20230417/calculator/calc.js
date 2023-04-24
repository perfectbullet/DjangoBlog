function ff1(){
    alert('imooc');
}

function ff2(){
    document.getElementById('btn2').onclick=function(){
        // alert('www.imooc.com');
        ff1();
    }
}