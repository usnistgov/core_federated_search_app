$(document).ready(function() {
    $('.refresh').on('click', refreshRepositoryOpenModal);
});


/**
 * Refresh form Token of a repository
 */
refreshRepositoryOpenModal = function(event) {
    $('#error-div').hide();

    var repositoryId = $(this).parent().attr('id');

    loadRefreshRepositoryForm(repositoryId);
};


/**
 * Load form Refresh Token of a repository
 */
loadRefreshRepositoryForm = function(repositoryId){
    $.ajax({
        url : refreshRepositoryUrl,
        type : "GET",
        dataType: "json",
        data : {
            'id': repositoryId
        },
        success: function(data){
            $("#refresh-repository-form").html(data.template);
            $('#refresh-repository-form').on('submit', {repository_id: repositoryId}, refreshRepositorySave);
            $('#refresh-repository-save').on('click', {repository_id: repositoryId}, refreshRepositorySave);
            $("#refresh-repository-modal").modal("show");
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

refreshRepositorySave = function(event) {
    $('#error-div').hide();
    $.ajax({
        url : refreshRepositoryUrl,
        type : "POST",
        dataType: "json",
        data : {
            'id': event.data.repository_id,
            'client_id': $("#id_client_id").val(),
            'client_secret': $("#id_client_secret").val(),
            'timeout': $("#id_timeout").val()
        },
        success: function(data){
            location.reload();
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

showErrorMessage = function(message){
    $('#error-div').show();
    $('#error-message').text(message);
};
