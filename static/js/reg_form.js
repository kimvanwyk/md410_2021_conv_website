$(document).ready(function() {
  $("#partner_none").change(function() {
    if ($(this).is(":checked") == true) {
      $('#partner_lion_div').hide();
      $('#partner_lion_fs').prop('disabled', '');
      $('#partner_non_lion_div').hide();
      $('#partner_non_lion_fs').prop('disabled', '');
    }
  });

  $("#partner_lion").change(function() {
    if ($(this).is(":checked") == true) {
      $('#partner_lion_div').show();
      $('#partner_lion_fs').removeAttr('disabled');
      $('#partner_non_lion_div').hide();
      $('#partner_non_lion_fs').prop('disabled', '');
    }
  });

  $("#partner_non_lion").change(function() {
    if ($(this).is(":checked") == true) {
      $('#partner_lion_div').hide();
      $('#partner_lion_fs').prop('disabled', '');
      $('#partner_non_lion_div').show();
      $('#partner_non_lion_fs').removeAttr('disabled');
    }
  });
  $("#partner_none").trigger("change");

  $("#full_reg").change(function() {
    if ($(this).is(":checked") == true) {
      $('#full_reg_div').show();
      $('#full_reg_fs').removeAttr('disabled');
      $('#partial_reg_div').hide();
      $('#partial_reg_fs').prop('disabled', '');
    }
  });

  $("#partial_reg").change(function() {
    if ($(this).is(":checked") == true) {
      $('#partial_reg_div').show();
      $('#partial_reg_fs').removeAttr('disabled');
      $('#full_reg_div').hide();
      $('#full_reg_fs').prop('disabled', '');
    }
  });
  $("#full_reg").trigger("change");

  $('.total').change(function () {
    var sum = 0;
    $('.total').each(function() {
      sum += (Number($(this).val()) * Number($(this).attr("cost")));
    });
    $('#total_cost').html("Total Cost: <strong>R" + sum + "</strong>");
  });
});
