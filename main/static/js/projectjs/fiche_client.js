jQuery(document).ready(function ($) {
  $(".clickable-row").click(function () {
    window.location = $(this).data("href");
  });
});

function current_status() {
  var current_status = document.getElementById("current_status");

  var buttons = document.getElementsByClassName("btn fiche");
  var instalment = document.getElementById("instalment");
  var add_contract = document.getElementById("add_contract");
  var div_ajout = document.getElementById("div_ajout");

  if (
    current_status.textContent == "Annulé" ||
    current_status.textContent == "Résilié"
  ) {
    for (var i = 0; i < buttons.length; i++) {
      var button = buttons[i];
      button.style.display = "none";
    }
    instalment.style.display = "block";
    //add_contract.style.width ="133px";
    //add_contract.style.display ="block";
  }
}

current_status();

function test_func(data) {
  return data;
}

// onclick get info sinister to update
$(".sinister_button").click(function () {
  currentRow = $(this).closest("tr");
  console.log(currentRow);
  link = $(this).val();
  console.log(link);
  var col_id = currentRow.find("td:eq(0)").text();
  var col_description = currentRow.find("td:eq(1)").text();
  var col_sinister_date = currentRow.find("td:eq(2)").text();
  var col_status = currentRow.find("td:eq(3)").text();

  var col_opposing_insurer = currentRow.find("td:eq(5)").text();
  var col_amount = currentRow.find("td:eq(6)").text();
  action = $("#info_sinister").find("form ").attr("action", link);
  action.val(link);
  description = $("#info_sinister form").find("#description");
  description.val(col_description);
  opposing_insurer = $("#info_sinister form").find("#opposing_insurer");
  opposing_insurer.val(col_opposing_insurer);
  amount = $("#info_sinister form").find("#amount");
  amount.val(col_amount);
  sinister_date = $("#info_sinister form").find("#sinister_date");
  sinister_date.val(col_sinister_date);
  if (col_status === "Invalide") {
    x = $("#info_sinister form").find("#Invalide").prop("checked", true);
  } else if (col_status === "Valide") {
    $("#info_sinister form").find("#Valide").prop("checked", true);
  } else if (col_status === "En Attente") {
    $("#info_sinister form").find("#En_Attente").prop("checked", true);
  } else {
    $("#info_sinister form").find("#None").prop("checked", true);
  }
});

// onclick get info contract to update
$(".contract_button").click(function () {
  currentRow = $(this).closest("tr");

  var col_id = currentRow.find("td:eq(0)").text();
  var col_creation_date = currentRow.find("td:eq(1)").text();
  var col_start_date = currentRow.find("td:eq(2)").text();
  var col_end_date = currentRow.find("td:eq(3)").text();
  var col_amount = currentRow.find("td:eq(4)").text();
  var col_contract_type = currentRow.find("td:eq(5)").text();
  var col_status = currentRow.find("td:eq(6)").text();

  creation_date = $("#info_contract form").find("#creation_date");
  creation_date.val(col_creation_date);
  contract_type = $("#info_contract form").find("#contract_type");
  contract_type.val(col_contract_type);
  end_date = $("#info_contract form").find("#end_date");
  end_date.val(col_end_date);
  amount = $("#info_contract form").find("#amount");
  amount.val(col_amount);
  start_date = $("#info_contract form").find("#start_date");
  start_date.val(col_start_date);

  if (col_status === "Annulé") {
    x = $("#info_contract form").find("#annulé_status").prop("checked", true);
  } else if (col_status === "Résilié") {
    $("#info_contract form").find("#résilié_status").prop("checked", true);
  } else if (col_status === "En Cours") {
    $("#info_contract form").find("#en_cours_status").prop("checked", true);
  } else if (col_status === "Activé") {
    $("#info_contract form").find("#activé_status").prop("checked", true);
  } else {
    $("#info_contract form").find("#none_status").prop("checked", true);
  }

  if (col_contract_type === "type 1") {
    $("#info_contract form").find("select").val("type 1");
  } else if (col_contract_type === "type 2") {
    $("#info_contract form").find("select").val("type 2");
  } else {
    $("#info_contract form").find("select").val("type 3");
  }
});

// onclick get info sinister to update
$(".indemnity_button").click(function () {
  currentRow = $(this).closest("tr");
  link = $(this).val();
  console.log(link);
  var col_id = currentRow.find("td:eq(0)").text();
  var col_sinister = currentRow.find("td:eq(1)").text();
  var col_amount = currentRow.find("td:eq(2)").text();
  var col_status = currentRow.find("td:eq(3)").text();
  var col_creation_date = currentRow.find("td:eq(4)").text();

  action = $("#info_indemnity").find("form ").attr("action", link);
  action.val(link);
  // description = $("#info_indemnity form").find('#description');
  // description.val(col_description)
  // opposing_insurer = $("#info_indemnity form").find('#opposing_insurer');
  // opposing_insurer.val(col_opposing_insurer)
  amount = $("#info_indemnity form").find("#amount");
  amount.val(col_amount);
  // sinister_date = $("#info_indemnity form").find('#sinister_date');
  // sinister_date.val(col_sinister_date)
  if (col_status === "Effectué") {
    $("#info_indemnity form").find("#Effectué").prop("checked", true);
  } else if (col_status === "Non Effectué") {
    $("#info_indemnity form").find("#Non_Effectué").prop("checked", true);
  } else {
    $("#info_indemnity form").find("#None").prop("checked", true);
  }
});
