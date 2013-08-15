function load_listings(page) {
  var url = $(location).attr('href');
  var search_string = $(location).attr('search');
  if (search_string) {
    if (page) {
      url += '&page=' + page;
    }
  }
  else {
    if (page) {
      url += '?page=' + page;
    }
  }
  $.get(
    url,
    function(response) {
      $('#listings').append(response);
    }
    );
}

$(document).ready(function() {
    load_listings();  // Get initial set
    $(window).scroll(function() {
        var break_point = ($(document).height() - ($(window).height()));
        if ($(window).scrollTop() == break_point) {
	  var next_page = $('#listing_tile li').last().attr('data-next');
	  if (next_page) {
	    load_listings(next_page);
	  }
        }
      });
  });
