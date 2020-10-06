var parallaxElements = $('.parallax'),
  parallaxQuantity = parallaxElements.length

$(window).on('scroll', function() {
  window.requestAnimationFrame(function() {
    var scrolled = $(window).scrollTop()
    if (scrolled > 0) {
      $('header').addClass('header-scrolled')
    } else { 
      $('header').removeClass('header-scrolled')
    }
    for (var i = 0; i < parallaxQuantity; i++) {
      var currentElement = parallaxElements.eq(i)
      if (scrolled < currentElement.parent().offset().top + $(window).height()) {
        currentElement.css({
          transform: 'translate3d(0,' + scrolled * + 0.5 + 'px, 0)',
        })
      }
    }
  })
})