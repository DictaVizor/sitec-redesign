$(window).on('load', function(){

    let loginForm = $('.login.form').form({
    }).api({
        on: 'submit',
        serializeForm: true,
        action: 'login',
        method: 'POST',
        beforeXHR: suiSetRequestHeaders,
        beforeSend: function(settings){
            return settings
        },
        onSuccess: function(response){
            window.location.href = '/sitec/panel/'
        },
        onError: function(){
            $('body').toast({
                message: 'Hubo un error al iniciar sesion.',
                class: 'error'
            })
        },
        onComplete: function(response, element, xhr){
        }
    })


    $('#login-button').on('click', function(){
        loginForm.form('submit')
    })
})