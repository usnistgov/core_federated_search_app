$(document).ready(function() {
    $('.delete').on('click', deleteRepositoryOpenModal);
    $('#delete-repository-yes').on('click', deleteRepository);
});

/**
 * Delete Repository and open the modal
 */
deleteRepositoryOpenModal = function(event)
{
    event.preventDefault();

    var repositoryId = $(this).parent().attr('id');
    var $repositoryRow = $(this).parent().parent();
    var repositoryName = $repositoryRow.find("td:first").text();

    $(".delete-repository-name").text(repositoryName);
    $("#delete-repository-id").val(repositoryId);
    $("#delete-repository-modal").modal("show");
};

/**
 * AJAX call, delete a repository
 * @param objectID id of the object
 */
deleteRepository = function(event){
    event.preventDefault();

    $.ajax({
        url : deleteRepositoryPostUrl,
        type : "GET",
        data: {
            "id": $("#delete-repository-id").val()
        },
        success: function(data){
            location.reload();
        }
    });
};