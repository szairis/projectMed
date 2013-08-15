$(document).ready(function () {
    $("#about #portrait").mouseenter(function(){
	$("#about #portrait #about_text").show();
    });
    $("#about #portrait").mouseleave(function(){
	$("#about #portrait #about_text").hide();
    });
  });