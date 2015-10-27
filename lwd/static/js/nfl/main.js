
var React = require('react');
var ReactDOM = require('react-dom');
var Select = require('react-select');

var MySelect = React.createClass({
    render: function() {
        var options = this.props.teams.map( function(team) {
            return {value: team, label: team};
        });
        return (
            <Select name="team-select" value="Select a Team" options={options} />
        );
    }    
});

var Notes = React.createClass({displayName: 'Notes',
    render: function() {
        return (
            <div className="row">
                <div className="col-sm-12">
                    <h2 className="orangeText">Notes4</h2>
                    <p className="blackText">Lower ranking is better (1 is best).</p>
                    <p className="blackText">Ranking based on average yards per game.</p>
                    <p className="blackText">Data from 1970 to 2014 for regular season games.</p>
                </div>
            </div>
        );
    }
});

var App = React.createClass({displayName: 'App',

    getInitialState: function() {
        return {teams: []};
    },

    componentDidMount: function() {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            success: function(teams) {
                this.setState({teams: teams});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },

    render: function() {
        return (
            <div className="nfl">
                <div className="row">
                    <div className="col-sm-12 row-top-buffer">
                        <MySelect teams={this.state.teams} />
                    </div>
                </div>
                <div className="row top-buffer">
                    <div className="col-sm-12">
                        <Graph />
                    </div>
                </div>
                <Notes />
            </div>
        );
    }
});

var Graph = React.createClass({

    componentDidMount: function() {
        var el = this.refs.chartNode;
        $(el).highcharts({
            title: {
                text: '{{ name }}',
                x: -20 //center
            },
            xAxis: {
                categories: ['a', 'b']
            },
            yAxis: {
                title: {
                    text: 'Ranking'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }],
                min: 0
            },
            legend: {
                layout: 'vertical',
                align: 'center',
                verticalAlign: 'bottom',
                borderWidth: 0
            },
            series: [{
                name: 'Offensive Ranking',
                color: '#0571b0',
                data: [1, 2]
            }, {
                name: 'Defensive Ranking',
                color: '#ca0020',
                data: [2, 3]
            }],
            credits: {
                enabled: false
            }
        });
    },

    render: function() {
        return (
            React.DOM.div({className: "chart-size", ref: "chartNode"})
        );
    }
});

ReactDOM.render(
    <App url="/nfl_teams" />,
    document.getElementById('content')
);
