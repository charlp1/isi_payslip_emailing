$(function () {

    var url = "payslip/upload";
    var uploadAlert = $( "#upload-alert" );
    var progressBar = $( "#progress .progress-bar" );
    var uploadTotalFiles = $( "#upload-total-files" );

    var uploadSuccessStatus = $( "#upload-success .status" );
    var uploadSuccessResult = $( "#upload-success .result" );
    var uploadSuccessContainer = $( "#upload-success" );

    var uploadErrorStatus = $( "#upload-error .status" );
    var uploadErrorResult = $( "#upload-error .result" );
    var uploadErrorContainer = $( "#upload-error" );

    var uploadStatusData = {
        "total": 0,
        "success": 0,
        "fail": 0
    };

    uploadAlert.hide();
    uploadSuccessContainer.hide();
    uploadErrorContainer.hide();

    $( "#fileupload" ).fileupload({
        url: url,
        dataType: "json",
        beforeSend: function( xhr, data ) {

            xhr.setRequestHeader( "X-CSRFToken", csrfToken );

            // Reset upload status and result
            uploadSuccessStatus.html( "" );
            uploadSuccessResult.html( "" );
            uploadErrorStatus.html( "" );
            uploadErrorResult.html( "" );
            uploadStatusData = {
                "total": 0,
                "success": 0,
                "error": 0
            };

            // Show upload result
            uploadSuccessContainer.show();
            uploadErrorContainer.show();

        },
        done: function ( e, data ) {

            console.log( "done:", data );
            var uploadSuccess = data.result.status === "ok";

            // List uploaded file
            data.context = $( "<tr/>" );
            $.each( data.files, function ( index, file ) {
                var node = $( "<td/>" ).html([
                    "<span>",
                        file.name,
                    "</span>"
                ].join( "" ));
                node.appendTo( data.context );
            });
            data.context.appendTo( "#upload-success .result" );

            // Update upload status
            if ( uploadSuccess ) {
                uploadStatusData.success++;
            } else {
                uploadStatusData.error++;
            }

            uploadSuccessStatus.html( "Uploaded: " + uploadStatusData.success );
            uploadErrorStatus.html( "Failed: " + uploadStatusData.error );

        },
        progressall: function ( e, data ) {

            var progress = parseInt( data.loaded / data.total * 100, 10 );

            progressBar.css(
                "width",
                progress + "%"
            );

            if ( progress == 100 ) {

                // Show upload result
                uploadAlert.show();

                // Reset progress bar
                // Hide upload result
                setTimeout( function() {
                    progressBar.css( "width", 0 );
                    uploadAlert.hide();
                }, 3000 );
            }
        }
    }).prop( "disabled", !$.support.fileInput )
        .parent().addClass( $.support.fileInput ? undefined : "disabled" );
});