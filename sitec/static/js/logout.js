$(window).on('load', function(){
    $('#logout-button').api({
        on:'click',
        action: 'logout',
        method: 'POST',
        beforeXHR: suiSetRequestHeaders,
        onSuccess: function(){
            window.location.href = '/sitec/login/'
        }
    })
})