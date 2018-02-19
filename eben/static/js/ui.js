$(document).ready(function() {

    var $form = $("#edit_profile");
    var $url = $form.attr('action');
    var $method = $form.attr('method');
    var $inner = $("#inner-form");

    $form.on('submit', function (e) {
        e.preventDefault();
        var $data = $(this).serialize();
        $.ajax({
            method: $method,
            url: $url,
            data: $data,
            async: false,
         //   dataType: 'json',
            success: function (data) {
              //  alert(data);
                $inner.append("<p class='good'>the form was filled properly</p>");
                location.reload();
            },
            error: function(xhr, ajaxOptions, thrownError) {
                   $inner.append("<p class='bad'>" + thrownError + xhr.statusText + xhr.responseText + "</p>");
            }
        });
    });
});

