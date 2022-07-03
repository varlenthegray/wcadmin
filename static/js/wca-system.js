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
}