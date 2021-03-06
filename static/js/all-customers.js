$(function() {
  let table = $("#customerDatatable").DataTable({
    dom: 'Blfrtip',
    buttons: {
      buttons: [
        { extend: 'copy', className: 'btn btn-outline-primary' },
        { extend: 'csv', className: 'btn btn-outline-primary' },
        { extend: 'excel', className: 'btn btn-outline-primary' },
        { extend: 'pdf', className: 'btn btn-outline-primary' },
        { extend: 'print', className: 'btn btn-outline-primary' },
      ]
    },
    lengthMenu: [
      [10, 25, 50, -1],
      [10, 25, 50, 'All'],
    ],
  });

  $("#dt_button_copy").on("click", function() {
    table.buttons('.buttons-copy').trigger();
    window.alert("Copied.");
  });

  $("#dt_button_csv").on("click", function() {
    table.buttons('.buttons-csv').trigger();
  });

  $("#dt_button_excel").on("click", function() {
    table.buttons('.buttons-excel').trigger();
  });

  $("#dt_button_pdf").on("click", function() {
    table.buttons('.buttons-pdf').trigger();
  });

  $("#dt_button_print").on("click", function() {
    table.buttons('.buttons-print').trigger();
  });
});