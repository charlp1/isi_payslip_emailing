// Table:
// name, email, active, send mail

var EmployeeInfo = React.createClass({

    "handleSelect": function( e ) {

        this.props.onClickSelectEmployee( this.props.info );

    },
    "render": function() {

        var index = this.props.index;
        var info = this.props.info;

        return (
            <tr key={ index + info.name }>
                <td>
                    <input type="checkbox"
                        checked={ info.selected }
                        onChange={ this.handleSelect } />
                </td>
                <td>{ info.send_status }</td>
                <td>{ info.name }</td>
                <td>{ info.email }</td>
                <td>{ info.active ? "active" : "inactive" }</td>
                <td>{ info.send_email ? "yes" : "no" }</td>
            </tr>
        );

    }

});

// Employee List
var EmployeeList = React.createClass({

    "handleSelectAll": function( e ) {

        this.props.onClickSelectAll();

    },
    "render": function() {

        var props = this.props;
        var employeeInfo = function( info, index ) {

            return (
                <EmployeeInfo index={ index }
                    info={ info }
                    onClickSelectEmployee={ props.onClickSelectEmployee } />
            );

        };
        console.log( "checkbox select all:", this.props.selectAll );
        console.log( "checkbox employees:", this.props.items );

        return (
            <table className="table table-striped table-hover table-bordered">
                <thead>
                    <tr>
                        <th>
                            <input type="checkbox"
                                checked={ this.props.selectAll }
                                onChange={ this.handleSelectAll } />
                        </th>
                        <th>Send Status</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Status</th>
                        <th>Send Email</th>
                    </tr>
                </thead>
                <tbody>
                    { this.props.items.map( employeeInfo ) }
                </tbody>
            </table>
        );
    }

});

// Send Email App
var EmailApp = React.createClass( {

    "componentWillMount": function() {

        amplify.request.define( "get_employee_list", "ajax", {
            "url": "/payslip/employee/",
            "dataType": "json",
            "type": "GET"
        });

        amplify.request.define( "send-email", "ajax", {
            "url": "/payslip/employee/",
            "dataType": "json",
            "type": "GET"
        });

    },
    "componentDidMount": function() {

        var self = this;
        var employees = this.getEmployeeList().then(
            function onSuccess( employeeList ) {
                self.setEmployeeList( employeeList );
            },
            function onError() {
                alert( "no employees" );
            }
        );

    },
    "componentWillUnmount": function() {

    },
    "getEmployeeList": function() {

        // Send status: ready, active, success, error
        var employees = [
                {
                    "name": "employee1",
                    "email": "test1@gmail.com",
                    "active": true,
                    "send_email": true,
                    "send_status": "ready",
                    "selected": true
                },
                {
                    "name": "employee2",
                    "email": "test2@gmail.com",
                    "active": true,
                    "send_email": true,
                    "send_status": "ready",
                    "selected": true
                },
                {"name": "employee3", "email": "test2@gmail.com", "active": true, "send_email": true, "send_status": "ready", "selected": true},
                {"name": "employee4", "email": "test2@gmail.com", "active": true, "send_email": true, "send_status": "ready", "selected": true},
                {"name": "employee5", "email": "test2@gmail.com", "active": true, "send_email": true, "send_status": "ready", "selected": true},
                {"name": "employee6", "email": "test2@gmail.com", "active": true, "send_email": true, "send_status": "ready", "selected": true},
                {"name": "employee7", "email": "test2@gmail.com", "active": true, "send_email": true, "send_status": "ready", "selected": true},
                {"name": "employee8", "email": "test2@gmail.com", "active": true, "send_email": true, "send_status": "ready", "selected": true},
                {"name": "employee9", "email": "test2@gmail.com", "active": true, "send_email": true, "send_status": "ready", "selected": true},
                {"name": "employee10", "email": "test2@gmail.com", "active": true, "send_email": true, "send_status": "ready", "selected": true},
                {"name": "employee11", "email": "test2@gmail.com", "active": true, "send_email": true, "send_status": "ready", "selected": true},
                {"name": "employee12", "email": "test2@gmail.com", "active": true, "send_email": true, "send_status": "ready", "selected": true},
                {"name": "employee13", "email": "test2@gmail.com", "active": true, "send_email": true, "send_status": "ready", "selected": true}
            ];
        var defer = $.Deferred();

        // TODO
        amplify.request({
            resourceId: "get_employee_list",
            data: {},
            success: function( data, status ) {

            },
            error: function( error, status ) {

            }
        });

        defer.resolve( employees );
        return defer.promise();

    },
    "setEmployeeList": function( employees ) {

        this.setState({
            "employees": employees
        });

    },
    "getInitialState": function() {

        return {
            "employees": [],
            "selectAll": true
        };

    },
    "sendEmailRequest": function( employee ) {

        var defer = $.Deferred();

        // TODO
        //amplify.request({
        //    resourceId: "send_email",
        //    data: {},
        //    success: function( data, status ) {
        //
        //    },
        //    error: function( error, status ) {
        //
        //    }
        //});

        setTimeout( function() {
            defer.resolve( employee );
        }, 3000 );

        return defer.promise();

    },
    "setEmployeeSendStatus": function( name, status ) {

        console.log( "set employee status:", name, status );
        var employees = _.map( this.state.employees, function( employee ) {
            if ( employee.name === name ) {
                employee.send_status = status;
            }
            return employee;
        });

        this.setState({
            "employees": employees
        });

    },
    "onClickSendEmail": function( e ) {

        e.preventDefault();

        alert( "send email" );

        // get list of employees checked
        // send request asynchronously
        var self = this;
        _.each( this.state.employees, function( employee ) {

            self.sendEmailRequest( employee ).then(
                function onSuccess() {
                    self.setEmployeeSendStatus( employee.name, "success" );
                },
                function onError() {
                    self.setEmployeeSendStatus( employee.name, "error" );
                }
            );

        });

    },
    "onClickSelectAll": function() {

        var prevState = this.state;
        var newSelectAll = !prevState.selectAll;

        var newEmployees = _.map( prevState.employees, function( employee ) {
            employee.selected = newSelectAll;
            return employee;
        });

        this.setState({
            "employees": newEmployees,
            "selectAll": newSelectAll
        });

    },
    "onClickSelectEmployee": function( employee ) {

        // Update employee select checkbox
        var employees = _.map( this.state.employees, function( currentEmployee ) {
            if ( currentEmployee.name === employee.name ) {
                currentEmployee.selected = !currentEmployee.selected;
            }
            return currentEmployee;
        });

        // Update select all employees checkbox
        var allEmployeesSelected = true;
        _.each( employees, function( currentEmployee ) {
            if ( !currentEmployee.selected ) {
                allEmployeesSelected = false;
            }
        });

        this.setState({
            "employees": employees,
            "selectAll": allEmployeesSelected
        });

        console.log( "select employee:", employee );

    },
    "render": function() {

        return (
            <div>
                <div id="send-email-table">
                    <EmployeeList items={ this.state.employees }
                        selectAll={ this.state.selectAll }
                        onClickSelectAll={ this.onClickSelectAll }
                        onClickSelectEmployee={ this.onClickSelectEmployee } />
                </div>
                <div id="send-email-button">
                    <button className="btn btn-success flex-auto"
                        onClick={ this.onClickSendEmail }>
                        Send Email
                    </button>
                </div>
            </div>
        );

    }

} );

React.render(
    <EmailApp />,
    document.getElementById( "email-app" )
);