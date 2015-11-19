$(function () {

    var url = "/payslip/upload/";

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

    var failedToUploadDate = "";
    var missingPayslipButton = $( "#missing-payslip-button" );
    var missingPayslipDate = $( "#missing-payslip-date" );
    var missingPayslipListContainer = $( "#missing-payslip-list" );
    var missingPayslipList = $( ".result", "#missing-payslip-list" );
    var missingPayslipStatus = $( ".status", "#missing-payslip-list" );

    /**
     * Request missing payslips
     */
    // Disable get missing payslip button
    missingPayslipButton.attr( "disabled", "disabled" );

    // Hide missing payslip date and list
    missingPayslipDate.hide();
    missingPayslipListContainer.hide();

    amplify.request.define( "get_missing_payslips", "ajax", {
        "url": "/payslip/api/missing_employee/",
        "dataType": "json",
        "type": "GET"
    });

    var requestMissingPayslip = function() {

        var defer = $.Deferred();

        amplify.request({
            resourceId: "get_missing_payslips",
            data: {
                "payslip": failedToUploadDate
            },
            success: function( data, status ) {
                defer.resolve( data, status );
            },
            error: function( error, status ) {
                defer.reject( error, status );
            }
        });

        return defer.promise();
    };

    var onGetMissingPayslips = function() {

        requestMissingPayslip().then(
            function onSuccess( response, status ) {
                var payslipList = _.map( response.data, function( payslip ) {
                    return '<li class="list-group-item">' + payslip + "</li>";
                });
                missingPayslipListContainer.show();
                missingPayslipList.html( payslipList.join("") );
                missingPayslipStatus.html( "Missing Payslip: " + payslipList.length );
            },
            function onError( error, status ) {
                missingPayslipListContainer.show();
                missingPayslipList.html( error && error.toString() );
                missingPayslipStatus.html( "Missing Payslip:" );
            }
        );

    };

    missingPayslipButton.on( "click", onGetMissingPayslips );

    /**
     * Upload payslip
     */
    // Hide upload status messages, and list
    uploadAlert.hide();
    uploadSuccessContainer.hide();
    uploadErrorContainer.hide();

    var updateProgressBar = function( progress ) {

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
    };

    var onUploadComplete = function( data ) {

        var result = data.result;
        var uploadSuccess = result.status === "ok";

        // List uploaded file
        data.context = $( '<li class="list-group-item" />' );
        $.each( data.files, function ( index, file ) {
            var node = $( "<div />" ).html([
                "<span>",
                    file.name,
                "</span>",
                "&nbsp;&nbsp;",
                '<span ',
                uploadSuccess ? 'class="alert-success" role="alert">' : 'class="alert-danger" role="alert">',
                    result.message,
                "</span>"
            ].join( "" ));
            node.appendTo( data.context );
        });

        // Update upload status
        uploadStatusData.total = data.originalFiles.length;
        if ( uploadSuccess ) {
            uploadStatusData.success++;
            data.context.appendTo( "#upload-success .result" );
        } else {
            uploadStatusData.error++;
            data.context.appendTo( "#upload-error .result" );
        }

        uploadSuccessStatus.html( "Uploaded: " + uploadStatusData.success + " / " + uploadStatusData.total );
        uploadErrorStatus.html( "Failed: " + uploadStatusData.error + " / " + uploadStatusData.total );

        // Update missing payslip button, date, and list
        failedToUploadDate = result.filename.split( " " )[ 0 ];
        missingPayslipDate.html( failedToUploadDate ).show();
        missingPayslipButton.removeAttr( "disabled", "" );
    };

    var initUploadResult = function() {

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

    };

    var initMissingPayslipsResult = function() {

        // Reset missing payslip button and date
        failedToUploadDate = "";
        missingPayslipDate.html( failedToUploadDate ).hide();
        missingPayslipButton.attr( "disabled", "disabled" );
        missingPayslipListContainer.hide();

    };

    $( "#fileupload" ).fileupload({
        url: url,
        dataType: "json",
        beforeSend: function( xhr, data ) {

            xhr.setRequestHeader( "X-CSRFToken", csrfToken );

            initUploadResult();

            initMissingPayslipsResult();

        },
        done: function ( e, data ) {

            onUploadComplete( data );

        },
        progressall: function ( e, data ) {

            var progress = parseInt( data.loaded / data.total * 100, 10 );

            updateProgressBar( progress );

        }
    }).prop( "disabled", !$.support.fileInput )
        .parent().addClass( $.support.fileInput ? undefined : "disabled" );
});