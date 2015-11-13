// Table:
// name, email, active, send mail

// Employee List
var EmployeeList = React.createClass({

    "render": function() {

        var employeeInfo = function( info, index ) {

            return (
                <tr key={ index + info.name }>
                    <td>{ info.name }</td>
                    <td>{ info.email }</td>
                    <td>{ info.active ? "active" : "inactive" }</td>
                    <td>{ info.send_email ? "yes" : "no" }</td>
                </tr>
            );

        };
        console.log( "items:", this.props.items );

        return (
            <table className="table table-striped table-hover table-bordered">
                <thead>
                    <tr>
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

        var employees = [
                {
                    "name": "employee1",
                    "email": "test1@gmail.com",
                    "active": true,
                    "send_email": true
                },
                {
                    "name": "employee2",
                    "email": "test2@gmail.com",
                    "active": true,
                    "send_email": true
                },
                {"name": "employee2", "email": "test2@gmail.com", "active": true, "send_email": true},
                {"name": "employee2", "email": "test2@gmail.com", "active": true, "send_email": true},
                {"name": "employee2", "email": "test2@gmail.com", "active": true, "send_email": true},
                {"name": "employee2", "email": "test2@gmail.com", "active": true, "send_email": true},
                {"name": "employee2", "email": "test2@gmail.com", "active": true, "send_email": true},
                {"name": "employee2", "email": "test2@gmail.com", "active": true, "send_email": true},
                {"name": "employee2", "email": "test2@gmail.com", "active": true, "send_email": true},
                {"name": "employee2", "email": "test2@gmail.com", "active": true, "send_email": true},
                {"name": "employee2", "email": "test2@gmail.com", "active": true, "send_email": true},
                {"name": "employee2", "email": "test2@gmail.com", "active": true, "send_email": true},
                {"name": "employee2", "email": "test2@gmail.com", "active": true, "send_email": true},
                {"name": "employee2", "email": "test2@gmail.com", "active": true, "send_email": true}
            ];
        var defer = $.Deferred();
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
            "employees": []
        };

    },
    "onClickSendEmail": function( e ) {

        e.preventDefault();

        alert( "send email" );
        // get list of employees checked
        // send request asynchronously
    },
    "render": function() {

        return (
            <div>
                <div id="send-email-table">
                    <EmployeeList items={ this.state.employees } />
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