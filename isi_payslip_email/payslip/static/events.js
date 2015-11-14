amplify.request.define( "resend_payslip", "ajax", {
    "url": "/payslip/api/send/",
    "dataType": "json",
    "type": "POST"
});

amplify.request.define( "see_logs", "ajax", {
    "url": "/payslip/api/logs/upload_sent/",
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

 $('#see_reports').on('click', function(){
     var pid = $('#pid').val();
     amplify.request({
         resourceId: 'see_logs',
         data: {
             'pid': pid
         },
         beforeSend: function( xhr, data ) {
             xhr.setRequestHeader( "X-CSRFToken", $.cookie(csrftoken) );
         },
         success: function(data){
             $('.logs_tbl').show();
             convert_table($('#upload_tbl'), data.payslip_uploaded);
             convert_table($('#sent_tbl'), data.payslip_sent);
             convert_table($('#unsent_tbl'), data.payslip_unsent);
         }
     })
 });

function convert_table(object, data){
    $(object).dataTable({
         data: data,
         "columns": [
             { "data": "name" },
             { "data": "filename" }
         ],
         bPaginate: false,
         bInfo: false,
         bFilter: false
     });
}