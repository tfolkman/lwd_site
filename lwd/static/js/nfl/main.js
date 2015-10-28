var React = require('react');
var ReactDOM = require('react-dom');
var Select = require('react-select');

var SelectGraph = React.createClass({

    getInitialState: function() {
        return {data: [], team: []};
    },

    componentDidMount: function() {
        var team = "San Francisco 49ers";
        this.setState({data: this.loadTeamData(team), team: team});
    },

    loadTeamData: function(team) {
        $.ajax({
            url: this.props.url,
            type: 'POST',
            data: JSON.stringify({'team': team}),
            contentType: 'application/json;charset=UTF-8',
            dataType: 'json',
            cache: false,
            success: function(data) {
                this.setState({data: data, team: team});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },

    render: function() {
        var options = this.props.teams.map( function(team) {
            return {value: team, label: team};
        });
        return (
            <div className="row">
                <div className="col-sm-3 row-top-buffer">
                    <Select name="team-select" value={this.state.team} options={options} onChange={this.loadTeamData}/>
                </div>
                <div className="row top-buffer">
                    <div className="col-sm-12">
                        <Graph data={this.state.data} team={this.state.team}/>
                    </div>
                </div>
            </div>
        );
    }    
});

var Notes = React.createClass({displayName: 'Notes',
    render: function() {
        return (
            <div className="row">
                <div className="col-sm-12">
                    <h2 className="orangeText">Notes</h2>
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
            url: this.props.teamUrl,
            dataType: 'json',
            cache: false,
            success: function(teams) {
                this.setState({teams: teams});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.teamUrl, status, err.toString());
            }.bind(this)
        });
    },

    render: function() {
        return (
            <div className="nfl">
                <SelectGraph teams={this.state.teams} url={this.props.dataUrl}/>
                <Notes />
            </div>
        );
    }
});

var Graph = React.createClass({

    componentDidUpdate: function() {
        var el = this.refs.chartNode;
        $(el).highcharts({
            title: {
                text: this.props.team,
                x: -20 //center
            },
            xAxis: {
                categories: this.props.data.years
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
                data: this.props.data.offense
            }, {
                name: 'Defensive Ranking',
                color: '#ca0020',
                data: this.props.data.defense
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
    <App teamUrl="/nfl_teams/" dataUrl="/nfl_team_data/" />,
    document.getElementById('content')
);
