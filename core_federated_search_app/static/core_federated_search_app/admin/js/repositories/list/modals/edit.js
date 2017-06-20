$(document).ready(function() {
    $('.edit').on('click', editRepositoryOpenModal);
    $('#edit-repository-form').on('submit', editRepositorySave);
    $('#edit-repository-save').on('click', editRepositorySave);
});


/**
 * Edit general information of a repository
 */
editRepositoryOpenModal = function(event) {
    event.preventDefault();

    var repositoryName = $(this).parent().siblings(':first').text();
    var repositoryId = $(this).parent().attr('id');

    $.ajax({
        url : editRepositoryPostUrl,
        type : "GET",
        dataType: "json",
        data : {
            'id': repositoryId,
            'name': repositoryName
        },
        success: function(data){
            $("#rename-form-receiver").html(data.template);
            $('#edit-error-div').hide();
            $("#edit-repository-modal").modal("show");
        },
        error:function(data){
            if (data.responseText != ""){
                showErrorMessage(data.responseText);
            }else{
                return (true);
            }
        }
    });
};

editRepositorySave = function(event) {
    event.preventDefault();

    $('#edit-error-div').hide();
    var formData = new FormData($( "#edit-repository-form" )[0]);

    $.ajax({
        url : editRepositoryPostUrl,
        type : "POST",
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function(data){
            location.reload();
        },
        error: function(data){
            $('#edit-error-message').html(data.responseText);
            $('#edit-error-div').show();
        }
    });
};
