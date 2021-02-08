$(document).ready(function(){
    var down = false;
    $('#bell').click(function(e){
        var color = $(this).text();
        if(down) {
            $('#box').css('height','0px');
            $('#box').css('opacity','0');
            disable();
            down = false;
        }
        
        else {
            $('#box').css('height','auto');
            $('#box').css('opacity','1');
            enable();
            down = true;
        }
    });
});

function enable() {
    $('#disabled').css('pointer-events', 'inherit');
}

function disable() {
    $('#disabled').css('pointer-events', 'none');
}