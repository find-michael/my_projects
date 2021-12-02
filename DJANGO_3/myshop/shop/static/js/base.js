$( document ).ready(function() {
    
    
    $('#nav-language').click(function() {
        if ($('section').hasClass('blurred')) {
            $('section, #content, footer').addClass('blurred-out')
            $('section, #content, footer').removeClass('blurred')
        } else { 
            $('section, #content, footer').removeClass('blurred-out')
            $('section, #content, footer').addClass('blurred') 
        }
        $('.language-list').toggle()
        $('#nav-language').toggleClass('nav-active')
    })
})