$(function() { 
    $('star').click(function() {
        var id = $(this).parents('div').attr('id');
        $(this).toggleClass('favorited');
        $.post('/yourUpdateUrl', 
               {'favorited': $(this).hasClass('favorited'), 'id': id},
                  function(data) { 
                     //some sort of update function here
                  });
         });
     });
});
