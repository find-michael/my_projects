$(document).ready(function() {
    
// GLOBAL VARIABLES / GLOBAL VARIABLES / GLOBAL VARIABLES / GLOBAL VARIABLES / GLOBAL VARIABLES / GLOBAL VARIABLES / GLOBAL VARIABLES / GLOBAL VARIABLES / GLOBAL VARIABLES

	var playlist_array = []
	var playlist_main = $('.playlist-main-container')
	var playlist_box = '<div class="playlist-box"><div class="playlist-img"></div><div class="playlist-title"></div></div>'
	var video_player = $('.video-player')[0]
	var video_autoplay = true
	var current_video_id = 0
	var window_height = $(window).height()
	var sorted = false
	var previous_video_id
	var search_results = $('.search-results')
	var max_num_of_search_results = 20
	var playlist_changed = false
	var number_of_new_added_elements = 15
	var existing_videos_number = 0
	var slide_spam_protection = false
	var hashtags_array = []
	var search_c = $('.search-container')
	var s_input = $('.search-input input[type="search"]')
	var filter_c = $('.filter-container')
	var settings_c = $('.settings-container')
	var video_array_options_changed = false
	var changed_options = []
	var position = $(window).scrollTop()
	var no_fixed = false
	var video_stop = false
	var was_video_paused
	var playlist_ended = false


	var strict_search = false // true means that if for example video has two hashtags ["one", "two"] and we filter off only one, the video wont show in playlist. Change to false if you want to show it
	var array_of_options = ['undefined', 'orchestra', 'hardbass', 'lovepoland', 'poland', 'piraci'] // set hashtag options (element in means that it wont show in playlist array. For example "array_of_options = ['orange', 'yellow']")


	video_player.volume = .3
	if (!strict_search) {$('.strict-soft-filter').addClass('no-strict')}
	$('.search-results').css('max-height', ($('.search-results').parent().outerHeight() - $('.search-input').outerHeight()))
	$('.filter-hashtags-checkboxes').css('max-height',
		($('.filter-container').height() - $('.filter-category').outerHeight() - $('.filter-hashtags-span').outerHeight(true) - $('.apply-filter-changes').outerHeight(true)))



// FUNCTIONS / FUNCTIONS / FUNCTIONS / FUNCTIONS / FUNCTIONS / FUNCTIONS / FUNCTIONS / FUNCTIONS / FUNCTIONS / FUNCTIONS / FUNCTIONS / FUNCTIONS / FUNCTIONS / FUNCTIONS

	function CreateHashtagsCheckboxes() {
		videos_array.filter(x => x.hashtags).map(x => x.hashtags).forEach(x => {x.forEach(x => {hashtags_array.push(x)})})
		function Unique(list) {
		    var result = []
		    $.each(list, function(i, e) {if ($.inArray(e, result) == -1) result.push(e)})
		    return result}
		hashtags_array = Unique(hashtags_array)
		hashtags_array.sort()
		DisplayHashtagsCheckboxes()
	}

	function DisplayHashtagsCheckboxes() {
		hashtags_array.map((x, y) => {
			var half = Math.round(hashtags_array.length/2)
			if (y + 1 <= half) {$('.filter-hashtags-checkboxes-left').append(HashtagsCheckboxesCore(x.toLowerCase()))}
			else {$('.filter-hashtags-checkboxes-right').append(HashtagsCheckboxesCore(x.toLowerCase()))}
		})
	}

	function HashtagsCheckboxesCore(x) {
		var z = (array_of_options.indexOf(x) > -1) ? '' : 'checked'
		var hashtag_checkbox = '<label class="hashtags-label">' +
									'<span>'+ x +'</span>' +
									'<input id="hashtag-'+ x +'" class="hashtags-checkbox checkbox-design" type="checkbox" '+ z +' data-checkbox="'+ x +'" data-checkbox-type="hashtag">' +
								'</label>'
		return hashtag_checkbox
	}

	function CreatePlaylist() {
		for (var i = 0; i < videos_array.length; i++) {
			if (videos_array[i].category == 'music' && $('.label-music input').is(":checked")) {ApplyOptions(i)}
			if (videos_array[i].category != 'music' && $('.label-other input').is(":checked")) {ApplyOptions(i)}
		}
		function ApplyOptions(i) {
			if (array_of_options.length != 0) {
				if (strict_search) {
					if (!array_of_options.some(r => videos_array[i].hashtags.includes(r))) {playlist_array.push(videos_array[i])}
				} else {
					if (videos_array[i].hashtags.some(r => array_of_options.indexOf(r) == -1)) {playlist_array.push(videos_array[i])}
				}
			} else {playlist_array.push(videos_array[i])}
		}
	}

	function DisplayPlaylist(searched_video) {
		window.scrollTo(0, 0)
		if (playlist_main.children().length >= 0) {
			playlist_main.empty()
			number_of_elements_added = 30;
		}
		if (searched_video) {
			Shuffle(playlist_array)
			var searched_video_id = playlist_array.findIndex(x => x.title.toLowerCase().indexOf(searched_video) > -1)
			var save_first_element = playlist_array[0]
			playlist_array[0] = playlist_array[searched_video_id]
			playlist_array[searched_video_id] = save_first_element
			sorted = false
		}
		DisplayPlaylistCore()
	}

	function DisplayPlaylistCore() {
		existing_videos_number = playlist_main.children('.playlist-box').length
		var loop_limit = existing_videos_number + number_of_new_added_elements
		if (existing_videos_number + number_of_new_added_elements > playlist_array.length) {loop_limit = playlist_array.length}
		for (var i = existing_videos_number; i < loop_limit; i++) {
			if (sorted) {
				var playlist_date = playlist_array[i].date_created.slice(0, 10).split("-").reverse().join("-")
				if (i == 0) {playlist_main.append('<div class="playlist-date"><span>' + playlist_date + '</span></div>')}
				if (i > 0 && !DatesAreOnSameDay(new Date(playlist_array[i-1].date_created), new Date(playlist_array[i].date_created)))
					playlist_main.append('<div class="playlist-date"><span>' + playlist_date + '</span></div>')
			}
			playlist_main.append(CreatePlaylistBox(playlist_array[i], i+1))
		}
		existing_videos_number = playlist_main.children('.playlist-box').length
		if (loop_limit == playlist_array.length) {playlist_main.append('<div class="copyright"><span>© 2019-2020 v2 Copyright: MaJK</span></div>')}
	}

	function CreatePlaylistBox(array, i) {
		var element =   '<div class="playlist-box">' + 
							'<div class="playlist-img">' + 
								'<img src="' + videos_file + array.title + '/thumbnail.jpg" alt="">' +
							'</div>' +
							'<div class="playlist-title">' +
								'<span>'+ array.title + '</span>' +
							'</div>' +
							'<div class="playlist-box-counter">' + i + ' / ' + playlist_array.length + '</div>' +
						'</div>'
		return element
	}

	function CreateSearchBox(array) {
		var element =  '<div class="search-box">' + 
							'<img src="' + videos_file + array.title + '/thumbnail.jpg" alt="">' +
							'<div class="search-title">' +
									'<span>'+ array.title + '</span>'
							'</div>' +
						'</div>'
		return element
	}

	function FirstLoad() {
		$('.video-play-icon').show()
		ChangeVideo(0, undefined, true)
	}

	function Shuffle(array) {
		// https://bost.ocks.org/mike/shuffle/
		var m = array.length, t, i;
		while (m) {
			i = Math.floor(Math.random() * m--);
			t = array[m];
			array[m] = array[i];
			array[i] = t;
		}
		return array;
	}

	function ChangeVideo(id, clicked, first_load) {
		if (PlaylistExist()) {
			if ($('.video-container')) {$('.video-container').show()}
			if (id >= playlist_array.length || playlist_changed) {
				if (!clicked) {id = 0}
				playlist_changed = false}
			video_player.src = videos_file + '/' + playlist_array[id].title + '/' + playlist_array[id].title + '.' + playlist_array[id].extension
			video_player.load();
			ChangeCurrentVideoID(id)
			CurrentlyActivePlaylistBox()
			if (!first_load && !playlist_ended) {PlayVideo()}
			if (playlist_ended) {playlist_ended = false}
		} else {$('.video-container').hide()}
	}

	function PlaylistExist() {
		if (playlist_array.length > 0) {return true}
		else {return false}
	}

	function PlayVideo(exception, dont_play) {
		if (video_autoplay || exception) {
			if (!dont_play) {video_player.play()}
		}
	}

	function PauseVideo(dont_pause) {
		if (!dont_pause) {video_player.pause()}
	}

	function ChangeCurrentVideoID(id) {
		previous_video_id = current_video_id
		current_video_id = id
		ChangeVideoTopTitles(current_video_id)
	}

	function ChangeVideoTopTitles(id) {
		$('.current-video-title').text(playlist_array[id].title)
		if (playlist_array[id + 1]) {
			$('.next-video-title').text('NEXT >> ' + playlist_array[id + 1].title)
		} else {$('.next-video-title').text('END OF PLAYLIST')}
		ChangeSoundWaveSrc(id)
	}

	function ChangeSoundWaveSrc(id) {
		$('.sound-wave').attr('src', videos_file + playlist_array[id].title + '/sound_wave.png')
	}

	function ScrollTop() {
		$('html, body').animate({ scrollTop: 0 }, 800)
	}

	function ScrollToElement(elem) {
		$('html, body').animate({scrollTop: playlist_main.children().eq(elem.index()).offset().top - (window_height/4)}, 800)
		if (!($('.found').length)) {
			elem.append('<div class="found"></div>')
			setTimeout(function(){ $('.found').remove() }, 1500);
		}
	}

	function PlaylistSortByDate() {
		playlist_array.sort((a, b) => new Date(b.date_created) - new Date(a.date_created))
		DisplayPlaylist()
	}

	const DatesAreOnSameDay = (first, second) =>
    	first.getFullYear() === second.getFullYear() &&
    	first.getMonth() === second.getMonth() &&
    	first.getDate() === second.getDate();


	function GetFormattedDate(date) {
		return date.getDate() + "-" + (date.getMonth() + 1) + "-" + date.getFullYear()
	}

	function CurrentlyActivePlaylistBox() {
		elem = playlist_main.children('.playlist-box').eq(current_video_id)
		if (!elem.length) {
			DisplayPlaylistCore()
			elem = playlist_main.children('.playlist-box').eq(current_video_id)}
		if (playlist_main.children('.active').length) {
			if (previous_video_id != current_video_id) {
				playlist_main.children('.active').removeClass('active')
				elem.addClass('active')
			}
		} else { elem.addClass('active') }
	}

	function DisplaySearchResults(array) {
		ClearSearchResults()
		$('.search-results-number span').text(array.length + ' results')
		if (array.length > 0) {
			for (var i = 0; i < array.length; i++) {search_results.append(CreateSearchBox(array[i]))}
		}
		if (array.length == 0) {search_results.append('<div class="search-not-found">Video not found</div>')}
	}

	function ClearSearchResults() {
		$('.search-results').empty()
		$('.search-results-number span').text('')
	}

	function NavbarOptionActive(x) {
		ShowActiveNavbarIcon(x)
		x = x.data('nav')
		if (x == 'search') {
			if ($('main').children('.slide-active')[0] != search_c[0]) {LetsGetCrazy()} 
			search_c.toggleClass('slide-active')
			if (search_c.hasClass('slide-active')) {s_input.select()}
			else {s_input.blur(), ClearSearchResults()}
		}
		if (x == 'filter') {
			if ($('main').children('.slide-active')[0] != filter_c[0]) {LetsGetCrazy()} 
			filter_c.toggleClass('slide-active')
		}
		if (x == 'settings') {
			if ($('main').children('.slide-active')[0] != settings_c[0]) {LetsGetCrazy()} 
			settings_c.toggleClass('slide-active')
		}
		if (x == 'go-to-playlist-start') {
			if (window.innerWidth <= 1200) {no_fixed = true}
			ScrollTop()}
		if (x == 'find-current' && playlist_main.children('.active').length) {
			if (window.innerWidth <= 1200) {no_fixed = true}
			ScrollToElement(playlist_main.children('.active'))}

		function LetsGetCrazy() {
			if (window.innerWidth >= 1200) {$('.video-section').addClass('increase-z-index')}
			$('main').children('.slide-active').addClass('slide-next')
			if ($('main').children('.slide-active')[0] == search_c[0]) {ClearSearchResults()}
			CloseActiveSlide()
			setTimeout(() => {
				$('main').children('.slide-next').removeClass('slide-next')
				$('.video-section').removeClass('increase-z-index')}
				, 200)
		}
		function ShowActiveNavbarIcon(y) {

			if (y.hasClass('nav-slideable') && y.children().first().attr("class") == 'nav-icon nav-icon-active') {
				CloseActiveSlideIcon()
			} else if (y.hasClass('nav-slideable')) {
				CloseActiveSlideIcon()
				y.children().first().attr("class", "nav-icon nav-icon-active")
				y.children('span').addClass('nav-icon-active')
				y.addClass('nav-div-triangle')
			}
		}
		if (no_fixed) {setTimeout(function() {no_fixed = false}, 800)}
	}

	function CloseActiveSlideIcon() {
		$('.nav-icon-div span').each(function() {$(this).removeClass('nav-icon-active')})
		$('.nav-slideable').each(function() {$(this).children().first().attr("class", "nav-icon")})
		$('.nav-slideable').each(function() {$(this).removeClass('nav-div-triangle')})
	}

	function CloseActiveSlide() {
		var slide_active = $('main').children('.slide-active')
		if (slide_active.length) {
			slide_active.removeClass('slide-active')
		}
	}

	function ChooseSearchResult(elem) {
		DisplayPlaylist(elem.find('span').text().toLowerCase())
        ChangeVideo(0)
        if (!video_autoplay) {PlayVideo(true)}
	}

	function ToggleNavGoToTop() {
		if ($(window).scrollTop() > window_height) {$('.nav-go-to-playlist-start').css('visibility', 'visible').addClass('nav-go-to-playlist-start-show')}
    	if ($(window).scrollTop() < window_height) {$('.nav-go-to-playlist-start').removeClass('nav-go-to-playlist-start-show').css('visibility', 'hidden')}
	}

	function ChangeOptions(option) {
		var found = changed_options.find(x => x == option)
		var found_index = changed_options.indexOf(found)
		if (found) {
			changed_options.splice( $.inArray(found, changed_options), 1 )
		} else {changed_options.push(option)}
		DoesOptionsChanged(changed_options.length > 0)
	}

	function DoesOptionsChanged(x) {
		if (x) {$('.apply-filter-changes button').addClass('apply-changes')}
		else {$('.apply-filter-changes button').removeClass('apply-changes')}
	}

	function ChangeArrayOfOptions() {

	RemoveGlobalOptions()
		changed_options.forEach(x => {
			if (array_of_options.indexOf(x) > -1) {
				array_of_options = jQuery.grep(array_of_options, y =>  y != x)
			} else {
				array_of_options.push(x)
			}
		})
	}

	function RemoveGlobalOptions() {
		changed_options = jQuery.grep(changed_options, x =>  x != 'music')
		changed_options = jQuery.grep(changed_options, x =>  x != 'strict')
		changed_options = jQuery.grep(changed_options, x =>  x != 'other')
	}

	function ApplyOptionChanges() {
		ChangeArrayOfOptions()
		playlist_array = []
		CreatePlaylist()
		if (sorted) {PlaylistSortByDate()}
		else {
			Shuffle(playlist_array)
			DisplayPlaylist()}
		FirstLoad()
		NavbarOptionActive($('.nav-filter'))
		$('.apply-filter-changes button').removeClass('apply-changes')
		changed_options = []
	}

	function IsCheckboxChecked(checkbox) {
		if (checkbox.is(":checked")) {return true}
		else {return false}
	}

	function FilterFastSettings(elem, settings) {

		if (settings == 'check-all') {
			$('input[data-checkbox-type="'+ elem +'"]').each(function() {
				if (!$(this).is(":checked")) {$(this).trigger('click')}
			})
		} else if (settings == 'toggle') {
			$('input[data-checkbox-type="'+ elem +'"]').trigger('click');
		} else if (settings == 'uncheck-all') {
			$('input[data-checkbox-type="'+ elem +'"]').each(function() {
				if ($(this).is(":checked")) {$(this).trigger('click')}
			})
		}
	}

	function SlideVideoSection(scroll) {
		if(scroll > position) {
			if (scroll > video_section_height) {$('.video-section').css('top', '-'+video_section_height+'px')}
		} else {
			if (scroll > video_section_height + 500) {
				if (window.innerWidth >= 1000) {$('.video-section').css('padding', '1rem 8rem 0 8rem')}
				if (no_fixed) { $('.video-section').css('position', '')
				} else {
					$('.video-section').css('top', '')
					$('.video-section').css('position', 'fixed')}
			}
		}
		position = scroll
		if (scroll <= video_section_height + 400) {
			$('.video-section').css('padding', '')
			$('.video-section').css('top', '')
			position = 0}
		if (scroll == 0) {$('.video-section').css('position', '')}
	}

	function ShowTimeOnSoundWave() {
		$('.sound-wave-time').prop('value', video_player.currentTime)
	}

	function ChangeFilterStrictSoft(elem) {
		(elem.hasClass('no-strict')) ? strict_search = true : strict_search = false
		elem.toggleClass('no-strict')
	}


	CreatePlaylist()
	Shuffle(playlist_array)
	DisplayPlaylist()
	FirstLoad()
	CreateHashtagsCheckboxes()

	var video_section_height = $('.video-section').outerHeight()
	if (window.innerWidth < 1200) {$('.playlist-section').css('margin-top', video_section_height+"px")}


// EVENTS / EVENTS / EVENTS / EVENTS / EVENTS / EVENTS / EVENTS / EVENTS / EVENTS / EVENTS / EVENTS / EVENTS / EVENTS / EVENTS / EVENTS / EVENTS / EVENTS / EVENTS / EVENTS


	window.onbeforeunload = function () {window.scrollTo(0, 0)}

	video_player.onended = function() {
		if (current_video_id + 1 >= playlist_array.length) {playlist_ended = true}
		(video_autoplay) ? ChangeVideo(current_video_id + 1) : PauseVideo()}

	video_player.onpause = function() {
		$('.video-play-icon').show()
		PauseVideo(true)}

	video_player.onplay = function() {
		$('.video-play-icon').hide()
		PlayVideo(true)}

	video_player.ontimeupdate = function() { if (!video_stop) {ShowTimeOnSoundWave()}}

	video_player.onloadedmetadata = function() {$('.sound-wave-time').prop('max', video_player.duration)}

	$('.sound-wave-time').mousedown(function() {
		was_video_paused = video_player.paused
		video_stop = true
		PauseVideo()
	})

	$('.sound-wave-time').click(function() {
		video_player.currentTime = $(this).val()
		video_stop = false
		if (!was_video_paused) {PlayVideo()}
	})

	$(window).resize(function(){
		$('.filter-hashtags-checkboxes').css('max-height', '')
		$('.filter-hashtags-checkboxes').css('max-height',
			($('.filter-container').height() - $('.filter-category').outerHeight() - $('.filter-hashtags-span').outerHeight(true) - $('.apply-filter-changes').outerHeight(true)))
		video_section_height = $('.video-section').outerHeight()
		if (window.innerWidth > 1200) {
		$('.video-section').css('top', '')
		$('.video-section').css('padding', '')
		$('.video-section').css('position', '')}
		if (window.innerWidth <= 1200) {$('.playlist-section').css('margin-top', video_section_height+"px")}
		else ($('.playlist-section').css('margin-top', ''))
		if (window.innerWidth <= 1000) {$('.video-section').css('padding', '')}
	})


	$(window).scroll(function (event) {
		var global_scroll = $(window).scrollTop();
		var playlist_position = $('.playlist-section').height();
		if (playlist_position - (global_scroll + window_height) < 300 && existing_videos_number != playlist_array.length) {DisplayPlaylistCore()}
		ToggleNavGoToTop()
		if (window.innerWidth < 1200) {
			SlideVideoSection(global_scroll)
		}
	})

	$('body').delegate('.playlist-box', 'click', function(){
        ChangeVideo($(this).index('.playlist-box'), true)
        if (!video_autoplay) {PlayVideo(true)}
	})

	$('.playlist-sort-random-items').click(function() {
		if (PlaylistExist()) {
			playlist_changed = true
			if (!sorted) {
				sorted = true
				PlaylistSortByDate()
				$('.playlist-sort').hide()
				$('.playlist-random').show()
			}
			else {
				sorted = false
				Shuffle(playlist_array)
				DisplayPlaylist()
				$('.playlist-random').hide()
				$('.playlist-sort').show()
			}
		}
	})

	$('.nav-icon-div').click(function() {
		(!$(this).hasClass('nav-slideable') && $('[class="nav-icon-active"]').length) ? '' : NavbarOptionActive($(this))
	})

	$('#autoplay-checkbox').click(() => {
		if ($('#autoplay-checkbox').is(':checked')) {video_autoplay = true}
		else {video_autoplay = false}
	})

	$('input[type="search"]').on('input', function() {
    	var value = $(this).val().toLowerCase()
    	if (value.length > 1) {
    		var results_array = playlist_array.filter(x => x.title.toLowerCase().indexOf(value) > -1);
    		DisplaySearchResults(results_array)
    	} else {ClearSearchResults()}
	})

	$(document).keydown(function(e) {
		if (e.which == 83) { // s
			if (!($('input[type="search"]').is(':focus'))) {
	        	e.preventDefault()
	        	NavbarOptionActive($('.nav-search'))
	    	}
	    } else if (e.which == 70) { // s
			if (!($('input[type="search"]').is(':focus'))) {
	        	e.preventDefault()
	        	NavbarOptionActive($('.nav-filter'))
	    	}
	    } else if (e.which == 13) { // enter
			if ($('input[type="search"]').is(':focus')) {
    			if ($('.search-box').length && !($('.search-not-found').length)) {
    				ChooseSearchResult($('.search-box').first())
    				NavbarOptionActive($('.nav-search'))
    			}
			}
		} else if (e.which == 27) { // escape
			if ($('main').find('.slide-active').length) {
				e.preventDefault()
				if ($('.search-container').hasClass('slide-active')) {NavbarOptionActive($('.nav-search'))}
	        	else {
	        		CloseActiveSlide()
	        		CloseActiveSlideIcon()}
			}
		} else if (e.which == 32) { // space
			if (!($('input[type="search"]').is(':focus'))) {
				if (PlaylistExist()) {
					e.preventDefault()
	        		video_player.blur()
	        		if (video_player.paused) {PlayVideo(true)}
	        		else if (!(video_player.paused)) {PauseVideo()}
        		}
			}
		}
	})


	$('body').delegate('.search-box', 'click', function() {
		ChooseSearchResult($(this))
		NavbarOptionActive($('.nav-search'))
	})

	$('body').delegate('.video-play-icon', 'click', function() {
		PlayVideo(true)
	})

	$('.nav-logo').click(() => location.reload())

	$('body').delegate('.hashtags-checkbox', 'click', function() {
		ChangeOptions($(this).data('checkbox').toLowerCase())
	})

	$('.category-checkbox').click(function() {
		ChangeOptions($(this).data('checkbox').toLowerCase())
	})

	$('.apply-filter-changes button').click(function() {
		if (changed_options.length > 0) {ApplyOptionChanges()}
	})

	$('.fast-settings div').click(function() {
		FilterFastSettings($(this).data('filter-fast-settings'), $(this).data('settings'))
	})

	$('.strict-soft-filter').click(function() {
		ChangeFilterStrictSoft($(this))
		ChangeOptions('strict')})


})
