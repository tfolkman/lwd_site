var React = require('react');
var ReactDOM = require('react-dom');
var Rcslider = require('rc-slider');

const slider_style = {width: 300, marginTop: 50};
const input_style = {width: 300, height: 50};
const button_style = {width: 50, height: 50, color: "black"};
const gen_style = {width: 150, height: 50, color: "black"};

var GenText = React.createClass({

    render: function() {
        return (
            <div className="row">
                <p className="gen-text">
                    {this.props.seed_text}
                </p>
            </div>
        );
    }    
})

var PresApp = React.createClass({

     getInitialState: function() {
        return {seed_text: '', gen_text: ''};
      },

      onChange: function(e) {
        this.setState({seed_text: e.target.value});
      },

      handleGenText: function(e) {
        $.ajax({
            url: "/gen_seed_text/",
            type: 'GET',
            contentType: 'application/json;charset=UTF-8',
            dataType: 'json',
            cache: false,
            success: function(data) {
                this.setState({seed_text: data});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.state.seed_text, status, err.toString());
            }.bind(this)
        });
      },

      handleSubmitText: function(e){
        e.preventDefault();
        $.ajax({
            url: "/gen_cand_text/",
            type: 'POST',
            data: JSON.stringify({'seed_text': this.state.seed_text}),
            contentType: 'application/json;charset=UTF-8',
            dataType: 'json',
            cache: false,
            success: function(data) {
                this.setState({gen_text: data['gen_text']});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.state.seed_text, status, err.toString());
            }.bind(this)
        });
      },

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
                        <button style={gen_style} onClick={this.handleGenText}>{'Generate for me'}</button>
                        <form onSubmit={this.handleSubmitText}>
                            <input onChange={this.onChange} value={this.state.seed_text} style={input_style} />
                            <button style={button_style}>{'GO'}</button>
                        </form>
                    </div>
                </div>
                <GenText seed_text={this.state.gen_text}/>
            </div>
        );
    }
});

ReactDOM.render(
    <PresApp />,
    document.getElementById('content')
);
