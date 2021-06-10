$(window).on('load', function(){
    $('#sidebar').sidebar('setting', 'transition', 'overlay')
    $('#toggle-sidebar').on('click', function(){
        $('#sidebar').sidebar('toggle')
    })
})