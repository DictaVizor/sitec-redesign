$(window).on('load', function(){
   let kardexManager = $('#kardex-manager').kardexManager()
   kardexManager.on('data-loader', function(){
       $('.shape').shape()
   })

})