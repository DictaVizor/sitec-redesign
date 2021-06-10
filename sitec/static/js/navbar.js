$(window).on('load', function(){
    $('#sidebar').sidebar('setting', 'transition', 'overlay')
    $('#toggle-sidebar').on('click', function(){
        $('#sidebar').sidebar('toggle')
    })

    $('#toggle-sidebar').visibility({
        type: 'fixed',
        offset: 15,
        zIndex: 1001,
    })
})