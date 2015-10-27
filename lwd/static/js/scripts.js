$(document).ready(function(){// activate scrollspy menu //
	
	$('body').scrollspy({
	  target: '#navbar-collapsible',
	  offset: 36
	});


	// smooth scrolling sections //
	$('a[href*=#]:not([href=#])').click(function() {
	    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
	      var target = $(this.hash);
	      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
	      if (target.length) {
	        $('html,body').animate({
	          scrollTop: target.offset().top - 35
	        }, 1000);
	        return false;
	      }
	    }
	});

});

$('.navbar-collapse a').click(function() {
	    $(".navbar-collapse").collapse('hide');
});

(function(i, s, o, g, r, a, m) {
	    i['GoogleAnalyticsObject'] = r;
	        i[r] = i[r] || function() {
			        (i[r].q = i[r].q || []).push(arguments)
	    }, i[r].l = 1 * new Date();
		    a = s.createElement(o),
	        m = s.getElementsByTagName(o)[0];
    a.async = 1;
        a.src = g;
	    m.parentNode.insertBefore(a, m)
})(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');

ga('create', 'UA-63651150-1', 'auto');
ga('send', 'pageview');

! function(d, s, id) {
	    var js, fjs = d.getElementsByTagName(s)[0],
		        p = /^http:/.test(d.location) ? 'http' : 'https';
	        if (!d.getElementById(id)) {
			        js = d.createElement(s);
				        js.id = id;
					        js.src = p + '://platform.twitter.com/widgets.js';
						        fjs.parentNode.insertBefore(js, fjs);
							    }
}(document, 'script', 'twitter-wjs');
