var windw = this;

$.fn.followTo = function ( pos ) {
  var $this = this,
  $window = $(windw);
  
  $window.scroll(function(e){
      if ($window.scrollTop() > pos) {
	$this.css({
	  position: 'fixed',
                top: 0,
	      });
      } else {
	$this.css({
	  position: 'absolute',
	      top: 120,
	      });
      }
    });
};

$('#sort_toolbar').followTo(120);