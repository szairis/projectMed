$(document).ready(function () {
    $("div .form_line:last-of-type").remove();
    $('#view_form input[type=submit]').remove();
    $('#view_form').submit(function (e) {
	e.preventDefault();
	var url = $(this).attr('action');
	url += "?";
	url += $(this).serialize();
	$.get(url, function(response) {
	    $('#listings #listing_tile').remove();
	    $('#listings p').remove();
	    setTimeout(function(){$('div#listings').append(response)},300);
	    window.history.pushState(response, "searched", url);
	  });
      });
    
    $('#view_form input[type=checkbox]').click(function () {
	$('#view_form').submit();
      });
    
    $('#view_form select').change(function(){
	$('#view_form').submit();
      });
  });