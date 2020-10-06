var clear_input = '<div class="clear-input"><img src="Icons/x-mark-32.png" alt=""></div>'

$(document).ready(function() {
	$('input[type=text]').each(function(index) {InputAddX(this)})
})

$('input[type=text]').on("keyup", function() {InputAddX(this)})

function InputAddX(element) {
	var elmt = $(element).parent().children('.clear-input')
	if ($(element).val() != '') {
		if (!(elmt.length)) {
			$(element).after(clear_input)
			$('.clear-input').on("click", function() {ClearInput($(this))})
		}
	}
	else {
		if (elmt.length) {elmt.remove()}
	}
}

function ClearInput(element) {
	element.prev().val('').focus()
	element.remove()
}


$('.show-password').on("click", function() {
	var elmt = $(this).parent().children('input')
	if (elmt.attr('type') == 'password') {
		elmt.attr('type', 'text') 
		$(this).children('img').attr("src","Icons/hide-30.png")
	} else if (elmt.attr('type') == 'text') {
		elmt.attr('type', 'password') 
		$(this).children('img').attr("src","Icons/show-30.png")
	}
	$(this).parent().children('input').focus()
})
