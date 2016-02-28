var React = require('react');
var ReactDOM = require('react-dom');
var Rcslider = require('rc-slider');

const slider_style = {width: 300, marginTop: 50};
const input_style = {width: 300, height: 50};
const button_style = {width: 50, height: 50, color: "black"};

var PresApp = React.createClass({
    render: function() {
        return (
            <div className="container">
                <h1 className="text-left bold-h1">Talk Like a Presidential Candidate</h1>
                <p className="line"></p>
                <div className="row">
                    <div className="col-sm-4">
                        <h2 className="bold-h2">Diversity</h2> 
                        <div style={slider_style}>
                            <Rcslider min={0.05} max={1.0} step={0.05}/>
                        </div>
                    </div>
                    <div className="col-sm-4">
                        <h2 className="bold-h2">Seed text of four words</h2> 
                        <input type="text" style={input_style}/>
                        <button style={button_style}> {'GO'} </button>
                    </div>
                </div>
            </div>
        );
    }
});

ReactDOM.render(
    <PresApp />,
    document.getElementById('content')
);
