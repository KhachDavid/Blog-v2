window.CSRF_TOKEN = "{{ csrf_token }}";

$(document).ready(function(){
    var down = true;
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

$(document).ready(function(event){
  // once like is clicked
  $(document).on('click', '#like', function(event){
    event.preventDefault();
    // take the primary key value of post
    var pk = $(this).attr('value');
    $.ajax({
      type: 'POST',
      url: "like",
      data: {'id': pk, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
      dataType: 'json',
      success: function(response) {
        $('#like-section').html(response['form'])
        console.log($('#like-section').html(response['form']));
      },
      error: function(rs, e) {
        console.log(rs.responseText);
      },
    });
  });
});

$(document).ready(function(event){
  $(document).on('click', '*[name="comment_id"]', function(event){
    event.preventDefault();
    var pk1 = $(this).attr('value'); // comment id
    var pk = $(this).attr('data-value'); // post id
    console.log(pk + " post id")
    console.log(pk1 + " comment id");
    var idname = '#comment-' + pk1;

    var buttonid = '#like-comment-' + pk1;

    console.log(idname);
    $.ajax({
      
      type: 'POST',
      url: $(this).attr('data-submit-url'),
      data: {'id': pk1, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
      dataType: 'json',
      success: function(json) {
        if (json.total_likes < 2) {
          $(idname).empty().prepend(json.total_likes + " հոգի հավանել է");
        }
        else {
          $(idname).empty().prepend(json.total_likes + " հոգի հավանել են");
        }

        if (!json.is_liked) {
          $(buttonid).empty().prepend("Հավանել");
          $(buttonid).removeClass("btn-danger").addClass("btn-primary");
          
        }
        else if (json.is_liked) {
          $(buttonid).empty().prepend("Չհավանել");
          $(buttonid).removeClass("btn-primary").addClass("btn-danger");
        }
      },
      error: function(rs, e) {
        console.log(rs.responseText);
      },
    });
  });
});

$(document).ready(function() {
  $(document).on('click', '#clickable-article', function(event){
    var url = $(this).attr('data-submit-url');
    console.log(url);
    location.href=url;
  });
});