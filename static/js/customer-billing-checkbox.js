let customerBillingCheckbox = {
  init: function(b_address_id, b_city_id, b_state_id, b_zip_id, j_address_id, j_city_id, j_state_id, j_zip_id, checkbox_id) {
    let fb_address = $("#" + b_address_id), fb_city = $("#" + b_city_id), fb_state = $("#" + b_state_id), fb_zip = $("#" + b_zip_id),
        fj_address = $("#" + j_address_id), fj_city = $("#" + j_city_id), fj_state = $("#" + j_state_id), fj_zip = $("#" + j_zip_id);

    function disableBilling(status) {
      if(status) {
        fb_address.prop('disabled', true);
        fb_city.prop('disabled', true);
        fb_state.prop('disabled', true);
        fb_zip.prop('disabled', true);

        fb_address.val(fj_address.val());
        fb_city.val(fj_city.val());
        fb_state.val(fj_state.val());
        fb_zip.val(fj_zip.val());
      } else {
        let fb_address_prev_val = fb_address.val(), fb_city_prev_val = fb_city.val(), fb_state_prev_val = fb_state.val(), fb_zip_prev_val = fb_zip.val();

        fb_address.prop('disabled', false).val(fb_address_prev_val);
        fb_city.prop('disabled', false).val(fb_city_prev_val);
        fb_state.prop('disabled', false).val(fb_state_prev_val);
        fb_zip.prop('disabled', false).val(fb_zip_prev_val);
      }
    }

    let same_billing_jobsite = $("#" + checkbox_id);

    same_billing_jobsite.on("change", function() {
      disableBilling(this.checked);
    });

    disableBilling(same_billing_jobsite.is(":checked"))

    fj_address.on("keyup", function() {
      if(same_billing_jobsite.is(":checked")) {
        fb_address.val(this.value);
      }
    });

    fj_city.on("keyup", function() {
      if(same_billing_jobsite.is(":checked")) {
        fb_city.val(this.value);
      }
    });

    fj_state.on("keyup", function() {
      if(same_billing_jobsite.is(":checked")) {
        fb_state.val(this.value);
      }
    });

    fj_zip.on("keyup", function() {
      if(same_billing_jobsite.is(":checked")) {
        fb_zip.val(this.value);
      }
    });
  }
};