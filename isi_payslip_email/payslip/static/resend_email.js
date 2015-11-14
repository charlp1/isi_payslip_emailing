 amplify.request.define( "resend_payslip", "ajax", {
    "url": "/payslip/api/send/",
    "dataType": "json",
    "type": "POST"
});

 function resend(pid){
     console.log(pid);
     $('#'+ pid).hide();
     $('#spinner'+ pid).show();
     amplify.request({
         resourceId: 'resend_payslip',
         data:{
             'pid': pid
         },
        beforeSend: function( xhr, data ) {
            xhr.setRequestHeader( "X-CSRFToken", $.cookie(csrftoken) );
        },
         success: function(data){
             if(data.status == 'ok'){
                 $('#spinner'+ pid).hide();
                 $('#success'+ pid).show();
             }
             else{
                 $('#spinner'+ pid).hide();
                 $('#error'+ pid).show();
             }

         }
     })
 }