/**
 * Created by panasco on 10/10/15.
 */

$(document).ready(function(){
    $('#employee_tab').on('click', function(){

        $.ajax({
            url: isi.apiUrls.employees,
            type: 'GET'
        }).done(function(data){
            $('#container_emp_table').html(data);
            $('#emp_table').dataTable({"iDisplayLength": 15});
        });
    });
});