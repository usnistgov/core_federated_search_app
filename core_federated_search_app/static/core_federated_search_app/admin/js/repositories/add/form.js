var $privateRepositoryCheckbox = $("input[role='switch']");

let updateForm = (isPrivateRepository) => {
    $(".private-repo").parent().toggle(isPrivateRepository)
}

$privateRepositoryCheckbox.on(
  "change", function(event) {
      updateForm(event.target.checked);
  }
);

$(document).ready(function() {
    $privateRepositoryCheckbox.prop("checked", false);
    updateForm(false);
})