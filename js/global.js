$(document).ready(function(){
	
	 $("div.navbar-collapse ul.nav li a").bind("click", function(e){
         // e.preventDefault();  e.stopPropagation();
		 $(this).parent().addClass("active");
         $("ul.nav li").removeClass("active");
         
         
     });	
	
});