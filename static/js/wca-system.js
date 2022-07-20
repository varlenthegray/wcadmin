// The purpose of this file is to handle system things such as Noty, etc

let wcaSystem = {
  show_notification: function(message, type, timeout = false) {
    new Noty({
      text: message,
      theme: 'bootstrap-v4',
      type: type,
      timeout: timeout
    }).show();
  },

  get_url_query: function() {
    let url = document.location.href;
    let qs = url.substring(url.indexOf('?') + 1).split('&');

    for(var i = 0, result = {}; i < qs.length; i++){
      qs[i] = qs[i].split('=');
      result[qs[i][0]] = decodeURIComponent(qs[i][1]);
    }

    return result;
  },

  setup_mde_editor: function(element, modal = true) {
    function db_insert_field(element_id, database_field) {
      $(element_id).on('click', function() {
        let text = simplemde.value();

        if(text.length > 0) {
          text += ' ' + database_field + ' ';
        } else {
          text += database_field;
        }

        simplemde.value(text);

        $("#insertDBField").modal('hide');
      });
    }

    let simplemde, editor = $(element);

    if (editor.length) {
      simplemde = new SimpleMDE({
        element: editor[0],
        toolbar: [
          "bold", "italic", "heading", "|", "code", "quote", "|", "unordered-list", "ordered-list", "|", "link",
          "image", "table", "horizontal-rule", "preview", "|",
          {
            name: 'insert_custom',
            action: function() {
              $("#insertDBField").modal('show');
            },
            className: 'fa fa-magic',
            title: 'Insert Database Field'
          }]
      });

      if(modal) {
        $(".template_container").parent().focus(function() {
          simplemde.codemirror.refresh();
        });
      } else {
        setTimeout(function() { simplemde.codemirror.refresh(); }, 20);
      }
    }

    db_insert_field('insert_first_name_mde', '[[customer.first_name]]');
    db_insert_field('insert_last_name_mde', '[[customer.last_name]]');
    db_insert_field('insert_company_name_mde', '[[customer.company]]');
    db_insert_field('insert_print_on_check_name_mde', '[[jobsite.print_on_check_name]]');
    db_insert_field('insert_email_mde', '[[customer.email]]');
    db_insert_field('insert_jobsite_name_mde', '[[jobsite.name]]');
    db_insert_field('insert_next_service_date_mde', '[[jobsite.next_service_date]]');

    return simplemde;
  }
}