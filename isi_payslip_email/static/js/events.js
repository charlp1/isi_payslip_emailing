/**
 * Created by panasco on 10/10/15.
 */

$(document).ready(function(){
    $('#employee_tab').on('click', function(){
        $.ajax({
            url: isi.apiUrls.employees
        }).done(function(data){
            alert('ajkfd');
        });
    });
});