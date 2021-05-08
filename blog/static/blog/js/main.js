/**
 * @author David Khachatryan
 * @copyright Copyright 2021, Mat Ognutyun
 * @license GPL
 * @version 2.0.0
 * @host David Khachatryan
 * @email dkhachatryan@wisc.edu
 * @status production
 */

window.CSRF_TOKEN = "{{ csrf_token }}";

/**
 * 
 */
$(document).ready(function(){
    $('#box').css('height','0px');
    $('#box').css('opacity','0');
    disable();
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

/**
 * 
 */
function enable() {
    $('#disabled').css('pointer-events', 'inherit');
}

/**
 * 
 */
function disable() {
    $('#disabled').css('pointer-events', 'none');
}

/**
 * 
 */
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

      /**
       * 
       * @param {*} response 
       */
      success: function(response) {
        $('#like-section').html(response['form'])
      },

      /**
       * 
       * @param {*} rs 
       * @param {*} e 
       */
      error: function(rs, e) {
    
      },
    });
  });
});

/**
 * 
 */
$(document).ready(function(event){
  $(document).on('click', '*[name="comment_id"]', function(event){
    event.preventDefault();
    var pk1 = $(this).attr('value'); // comment id
    var pk = $(this).attr('data-value'); // post id
    var idname = '#comment-' + pk1;

    var buttonid = '#like-comment-' + pk1;

    console.log(idname);
    $.ajax({
      
      type: 'POST',
      url: $(this).attr('data-submit-url'),
      data: {'id': pk1, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
      dataType: 'json',

      /**
       * 
       * @param {*} json 
       */
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

      /**
       * 
       */
      error: function(rs, e) {
      
      },
    });
  });
});

/**
 * 
 */
$(document).ready(function() {
  $(document).on('click', '#clickable-article', function(event){
    var url = $(this).attr('data-submit-url');
    location.href=url;
  });
});


/**
 * 
 * @param {*} post_pk 
 */
function upvoteClick(post_pk) {
  var current_element = document.getElementById("like-dislike-button-" + post_pk + "-like");
  current_element.style.animation = "";
  $.ajax({

    type: 'POST',
    url: "post/" + post_pk + "/like",
    data: {'id': post_pk, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
    dataType: 'json',

    /**
     * 
     * @param {*} json 
     */
    success: function(json) {
      var like_count = document.querySelectorAll(".like-count-" + post_pk);

      like_count.forEach( (b) => {
        b.innerHTML = json['total_likes'] - json['total_dislikes'];

        // change the emoji to 100%

        //current_element.className = "animate-like-buttons";
        toggleLike(current_element);
        initializeDislike(document.getElementById("like-dislike-button-" + post_pk + "-dislike"));
        current_element.style.animation = "like 0.8s forwards";

      });
    },

    /**
     * 
     * @param {*} rs 
     * @param {*} e 
     */
    error: function(rs, e) {
      var like_count = document.querySelectorAll(".like-count-" + post_pk);

      like_count.forEach( (b) => {
        b.innerHTML = 0;
      });
    },
  });
}

/**
 * 
 * @param {*} post_pk 
 */
function downvoteClick(post_pk) {
  var current_element = document.getElementById("like-dislike-button-" + post_pk + "-dislike");
  current_element.style.animation = "";

  $.ajax({
    type: 'POST',
    url: "post/" + post_pk + "/dislike",
    data: {'id': post_pk, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
    dataType: 'json',

    /**
     * 
     * @param {*} json 
     */
    success: function(json) {
      var like_count = document.querySelectorAll(".like-count-" + post_pk);

      like_count.forEach( (b) => {
        b.innerHTML = json['total_likes'] - json['total_dislikes'];
      });

      // change the emoji to the like button
      toggleDislike(current_element);
        
      initializeLike(document.getElementById("like-dislike-button-" + post_pk + "-like"));
      current_element.style.animation = "like 0.8s forwards";
    },

    /**
     * 
     * @param {*} rs 
     * @param {*} e 
     */
    error: function(rs, e) {
      var like_count = document.querySelectorAll(".like-count-" + post_pk);

      like_count.forEach( (b) => {
        b.innerHTML = 0;
      });
    },

  });
}

const like_state_class = "vote upvote";
const liked_state_class = "vote upvote-active";

/**
 * 
 * @param {*} current_element 
 */
function toggleLike(current_element) {
  current_element.className === like_state_class ?
                                current_element.className = liked_state_class :
                                current_element.className = like_state_class;

}

const dislike_state_class = "vote downvote";
const disliked_state_class = "vote downvote-active";

/**
 * 
 * @param {*} current_element 
 */
function toggleDislike(current_element) {
  current_element.className === dislike_state_class ?
                                current_element.className = disliked_state_class :
                                current_element.className = dislike_state_class;
}

/**
 * 
 * @param {*} current_element 
 */
function initializeLike(current_element) {
  current_element.className = like_state_class;
  current_element.style.animation = "";
}

/**
 * 
 * @param {*} current_element 
 */
function initializeDislike(current_element) {
  current_element.className = dislike_state_class;
  current_element.style.animation = "";
}