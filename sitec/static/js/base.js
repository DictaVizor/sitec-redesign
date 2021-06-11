$(window).on('load', function(){
    let syncSitecForm = $('.sync.sitec.form').form({

    }).api({
        on: 'submit',
        action: 'sync sitec',
        method: 'POST',
        beforeXHR: suiSetRequestHeaders,
        serializeForm: true,
        beforeSend: function(settings){
            return settings
        },
        onSuccess: function(){
            window.location.href = '/sitec/panel/'
        },
        onError: function(){
            $('body').toast({
                message: 'Hubo un error al sincronizar los datos. Por favor, intenta de nuevo mas tarde.',
                class: 'error'
            })
        }
    })
    let sitecModal = $('.sync.sitec.modal').modal({
        onApprove: function(){
            syncSitecForm.form('submit')
            return false
        }
    })
    let syncSitecButton = $('.sync.sitec.button')
    syncSitecButton.on('click', function(){
        sitecModal.modal('show')
    })



})