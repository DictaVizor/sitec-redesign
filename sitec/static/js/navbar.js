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

    $('#sidebar').api({
        on: 'now',
        action: 'get user profile',
        beforeXHR: suiSetRequestHeaders,
        onSuccess: function(response){
            $('#sidebar').find('#student-name').html(response.sitec_data.panel_data.name)
            $('#sidebar').find('#control-number').html(response.sitec_data.panel_data.control_number)
        }
    })

})