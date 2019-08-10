$(document).ready(function() {
  $("#partner_none").change(function() {
    if ($(this).is(":checked") == true) {
      $('#partner_lion_div').hide();
      // $('#otherField').removeAttr('required');
      // $('#otherField').removeAttr('data-error');
      $('#partner_non_lion_div').hide();
      // $('#otherFieldDiv').show();
      // $('#otherField').attr('required', '');
      // $('#otherField').attr('data-error', 'This field is required.');
    }
  });
  $("#partner_none").trigger("change");

  $("#partner_lion").change(function() {
    if ($(this).is(":checked") == true) {
      $('#partner_lion_div').show();
      $('#partner_non_lion_div').hide();
    }
  });
  // $("#partner_lion").trigger("change");

  $("#partner_non_lion").change(function() {
    if ($(this).is(":checked") == true) {
      $('#partner_lion_div').hide();
      $('#partner_non_lion_div').show();
    }
  });
  // $("#partner_non_lion").trigger("change");

  $("#seeAnotherFieldGroup").change(function() {
    if ($(this).val() == "yes") {
      $('#otherFieldGroupDiv').show();
      $('#otherField1').attr('required', '');
      $('#otherField1').attr('data-error', 'This field is required.');
      $('#otherField2').attr('required', '');
      $('#otherField2').attr('data-error', 'This field is required.');
    } else {
      $('#otherFieldGroupDiv').hide();
      $('#otherField1').removeAttr('required');
      $('#otherField1').removeAttr('data-error');
      $('#otherField2').removeAttr('required');
      $('#otherField2').removeAttr('data-error');
    }
  });
  $("#seeAnotherFieldGroup").trigger("change");
});
