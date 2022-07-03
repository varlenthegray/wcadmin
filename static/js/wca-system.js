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
  }
}