// Table:
// name, email, active, send mail

var EmployeeInfo = React.createClass({displayName: "EmployeeInfo",

    "handleSelect": function( e ) {

        this.props.onClickSelectEmployee( this.props.info );

    },
    "render": function() {

        var index = this.props.index;
        var info = this.props.info;
        var send_status = info.send_status;
        var sendStatusIcon = {
            "ready": "",
            "sending": (React.createElement("i", {className: "glyphicon glyphicon-refresh icon-refresh-animate"})),
            "success": (React.createElement("i", {className: "glyphicon glyphicon-ok"})),
            "error": (React.createElement("i", {className: "glyphicon glyphicon-remove"})),
            "disable": ""
        };
        var rowHighlight = {
            "ready": "active",
            "sending": "info",
            "success": "success",
            "error": "danger"
        };
        var select = send_status === "success" || send_status === "disable" ? "" :
            ( React.createElement("input", {type: "checkbox", checked:  info.selected, onChange:  this.handleSelect}) );
        var link = info.file_url ? (React.createElement("a", {href:  info.file_url, target: "_blank"}, "PDF")) : "";

        return (
            React.createElement("tr", {key:  index + info.name, 
                className:  rowHighlight[ send_status] }, 
                React.createElement("td", null, 
                    select 
                ), 
                React.createElement("td", null, index ), 
                React.createElement("td", null,  info.name), 
                React.createElement("td", null,  info.email), 
                React.createElement("td", null, 
                    link 
                ), 
                React.createElement("td", null, 
                     sendStatusIcon[ send_status] 
                )
            )
        );

    }

});

// Employee List
var EmployeeList = React.createClass({displayName: "EmployeeList",

    "handleSelectAll": function( e ) {

        this.props.onClickSelectAll();

    },
    "render": function() {

        var props = this.props;
        var employeeInfo = function( info, index ) {

            return (
                React.createElement(EmployeeInfo, {index: index, 
                    info: info, 
                    onClickSelectEmployee:  props.onClickSelectEmployee})
            );

        };

        return (
            React.createElement("table", {className: "table table-striped table-hover table-bordered"}, 
                React.createElement("thead", null, 
                    React.createElement("tr", null, 
                        React.createElement("th", null, 
                            React.createElement("input", {type: "checkbox", 
                                checked:  this.props.selectAll, 
                                onChange:  this.handleSelectAll})
                        ), 
                        React.createElement("th", null), 
                        React.createElement("th", null, "Name"), 
                        React.createElement("th", null, "Email"), 
                        React.createElement("th", null, "Link"), 
                        React.createElement("th", null, "Send Status")
                    )
                ), 
                React.createElement("tbody", null, 
                     this.props.items.map( employeeInfo) 
                )
            )
        );
    }

});

// Send Email App
var EmailApp = React.createClass( {displayName: "EmailApp",

    "componentWillMount": function() {

        amplify.request.define( "send_email", "ajax", {
            "url": "/payslip/api/send/",
            "dataType": "json",
            "type": "POST"
        });

    },
    "componentDidMount": function() {

    },
    "componentWillUnmount": function() {

    },
    "setEmployeeList": function( employees ) {

        console.log( "set employee list:", employees.slice() );

        var newEmployees = _.map( employees, function( employee ) {

            employee.send_status = employee.send_email ? "ready" : "disable";
            employee.selected = true;

            return employee;

        });

        newEmployees = _.filter( newEmployees, function( employee ) {
            return !employee.status;
        });

        this.setState({
            "employees": newEmployees,
            "selectAll": true
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

        console.log( "send email request:", employee.payslip_id, employee );

        amplify.request({
            resourceId: "send_email",
            data: {
                "pid": employee.payslip_id
            },
            success: function( data, status ) {
                defer.resolve( data, status );
            },
            error: function( error, status ) {
                defer.resolve( error, status );
            }
        });

        return defer.promise();

    },
    "setEmployeeSendStatus": function( data, status ) {

        var updatedPayslipId = data.data.id;
        var employees = _.map( this.state.employees, function( employee ) {
            if ( employee.payslip_id == updatedPayslipId ) {
                employee.send_status = status;
            }
            return employee;
        });

        this.setState({
            "employees": employees
        });

    },
    "sendEmailToEmployee": function( employees ) {

        var employeeList = employees.slice();
        var employee = employeeList.shift();
        var deferred = $.Deferred();
        var self = this;
        var send_status = employee.send_status;
        var emailNotSent = send_status === "ready" || send_status === "error";
        var sendEmail = employee.selected && employee.send_email && emailNotSent;

        if ( sendEmail ) {

            self.setEmployeeSendStatus({
                "data": { "id": employee.payslip_id },
                "status": "sending"
            }, "sending");

            setTimeout(function () {
                self.sendEmailRequest(employee).then(
                    function onSuccess(data, status) {
                        self.setEmployeeSendStatus(data, status);
                        deferred.resolve( employeeList );
                    },
                    function onError(error, status) {
                        self.setEmployeeSendStatus(error, status);
                        deferred.resolve( employeeList );
                    }
                );
            }, 100);

        } else {

            this.setEmployeeSendStatus({
                "data": { "id": employee.payslip_id },
                "status": "error"
            }, "error");

        }

        return deferred.promise();
    },
    "sendEmail": function( employees ) {

        var employeeList = _.isEmpty( employees ) ? this.state.employees : employees;

        // get list of employees checked
        // send request asynchronously
        var self = this;
        var sendEmailDone = this.sendEmailToEmployee( employeeList );

        sendEmailDone.then( function onSuccess( newEmployeeList ) {
            setTimeout( function() {
                if ( !_.isEmpty(newEmployeeList)) {
                    self.sendEmail(newEmployeeList);
                }
            }, 1000 );
        }, function onError( newEmployeeList ) {
            setTimeout( function() {
                if ( !_.isEmpty(newEmployeeList)) {
                    self.sendEmail(newEmployeeList);
                }
            }, 1000 );
        });
    },
    "onClickSendEmail": function( e ) {

        e.preventDefault();

        if ( !_.isEmpty( this.state.employees ) ) {

            var employees = _.filter( this.state.employees, function( employee ) {
                return employee.selected && employee.send_email &&
                    (employee.send_status === "ready" || employee.send_status === "error");
            });

            this.sendEmail( employees );

        }

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

    },
    "render": function() {

        return (
            React.createElement("div", {id: "email-app-inner-container"}, 
                React.createElement("div", {id: "send-email-table"}, 
                    React.createElement(EmployeeList, {items:  this.state.employees, 
                        selectAll:  this.state.selectAll, 
                        onClickSelectAll:  this.onClickSelectAll, 
                        onClickSelectEmployee:  this.onClickSelectEmployee})
                ), 
                React.createElement("div", {id: "send-email-button"}, 
                    React.createElement("button", {className: "btn btn-success flex-auto", 
                        disabled:  _.isEmpty( this.state.employees), 
                        onClick:  this.onClickSendEmail}, 
                        "Send Email"
                    )
                )
            )
        );

    }

} );

var emailApp = React.render(
    React.createElement(EmailApp, null),
    document.getElementById( "email-app" )
);