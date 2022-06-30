// The purpose of this file is to manage all types of string manipulations needed in JS
// This was first implemented and is heavily used in all_jobsites_card.html

let stringManipulations = {
  truncate: function(str, max) {
    max = max - 2; // remove 2 characters from the total max count (to account for hellip and 0 offset)
    let not_found = 'N/A';

    if(str !== null && str !== undefined) {
      if(str.length > max) {
        let truncated_string = jQuery.trim(str).substring(0, max) + "&hellip;";

        return '<abbr title="' + str + '">' + truncated_string + '</abbr>';
      } else if(jQuery.trim(str).length === 0) {
        return not_found;
      } else {
        return str;
      }
    }  else {
      return not_found;
    }
  }
}