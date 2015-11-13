/**
 * Created by panasco on 10/10/15.
 */

$(document).ready(function(){

    var employeeTableContainer = $( '#container_emp_table' );
    var employeeTable = $( '#emp_table' );

    var updateEmployeeTable = function() {

        $.ajax({
            url: isi.apiUrls.employees,
            type: 'GET'
        }).done(function(data){
            employeeTableContainer.html(data);
            employeeTable.dataTable({"iDisplayLength": 15});
        });
    };

    $( '#employee_tab' ).on( 'click', updateEmployeeTable );

});