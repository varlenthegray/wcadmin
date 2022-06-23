$(function() {
  let job_site_table = $("#customerDatatable").DataTable({
    dom: 'lfrtip',
    scrollY: 480,
    // ajax: '/job_sites/all_job_sites_json',
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
    fixedHeader: {
      header: true
    },
  });

  $("#dt_button_copy").on("click", function() {
    job_site_table.buttons('.buttons-copy').trigger();
    window.alert("Copied.");
  });

  $("#dt_button_csv").on("click", function() {
    job_site_table.buttons('.buttons-csv').trigger();
  });

  $("#dt_button_excel").on("click", function() {
    job_site_table.buttons('.buttons-excel').trigger();
  });

  $("#dt_button_pdf").on("click", function() {
    job_site_table.buttons('.buttons-pdf').trigger();
  });

  $("#dt_button_print").on("click", function() {
    job_site_table.buttons('.buttons-print').trigger();
  });
});