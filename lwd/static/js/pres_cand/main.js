var React = require('react');
var ReactDOM = require('react-dom');
var Rcslider = require('rc-slider');

const slider_style = {width: 300, marginTop: 50};
const input_style = {width: 300, height: 50};
const button_style = {width: 50, height: 50, color: "black"};
const gen_style = {width: 150, height: 50, color: "black"};

var ErrorGenText = React.createClass({
    render: function() {
        return (
            <div className="row">
                <p className="error-gen-text">
                    {this.props.char}
                </p>
            </div>
        );
    }
})

var SuccessGenText = React.createClass({
    render: function() {
        return (
            <div className="row">
                <p className="gen-text">
                    {this.props.gen_text}
                </p>
            </div>
        );
    }    
})

var GenText = React.createClass({

    render: function() {
        var genText;
        if (this.props.error_flag == 1) {
            genText = <ErrorGenText char={this.props.gen_text} />;
        } else {
            genText = <SuccessGenText gen_text={this.props.gen_text} />;
        }
        return (
            <p>
            {genText}
            </p>
        );
    }    
})

var PresApp = React.createClass({

     getInitialState: function() {
        return {seed_text: '', gen_text: '', diversity: '1.0', gen_error: '0'};
      },

      onChange: function(e) {
        this.setState({seed_text: e.target.value});
      },

    onSliderChange: function(value) {
        this.setState({
            diversity: value,
        });
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
            data: JSON.stringify({'seed_text': this.state.seed_text,
                                    'diversity': this.state.diversity}),
            contentType: 'application/json;charset=UTF-8',
            dataType: 'json',
            cache: false,
            success: function(data) {
                this.setState({gen_text: data['gen_text'], gen_error: data['error_flag']});
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
                <h2 className="text-left bold-h2">An LSTM Language Model</h2>
                <p className="line"></p>
                <div className="row">
                    <div className="col-sm-4">
                        <h2 className="bold-h2">Diversity</h2> 
                        <div style={slider_style}>
                            <Rcslider min={0.05} max={1.0} step={0.05} defaultValue={1.0}
                                onChange={this.onSliderChange} />
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
                <p className="line"></p>
                <h2 className="bold-h3">generated text:</h2>
                <GenText gen_text={this.state.gen_text} error_flag={this.state.gen_error}/>
                <p className="line"></p>
                <p className="bold-p">
                    I have been wanting to try my hand at an LSTM model for a while now. If you are not familiar with LSTM networks, I would highly recommend <a href="http://colah.github.io/posts/2015-08-Understanding-LSTMs/">this introduction</a>. One thing this model can be used for is a language model. The goal of a language model is to predict the next word given a number of previous words. For example, given "I will win the" what is a probable next word? Perhaps race? 
                </p>
                <p className="bold-p"> 
                    I decided it would be interesting to try and develop a language model that speaks like a Presidential candidate. To do so, I scraped the transcipts from some presidential (republican and democratic) debates. The code for this can be found <a href="https://github.com/tfolkman/learningwithdata/blob/master/Get_Debate_Data.ipynb">here.</a> To be honest, I didn't spend much time confirming an exact scrap of the data and simply split sentences on spaces to get words.
                </p>
                <p className="bold-p"> 
                    To build the model, I used <a href="http://keras.io/">Keras.</a> This is my first time using Keras and I found it to be pretty nice. It was a small amount of code to build my model and was easy to experiment with. The code used to build my model can be found <a href="https://github.com/tfolkman/learningwithdata/blob/master/LSTM_Debate_Model.ipynb">here.</a> I built the model to predict a word given the 5 previous words. You can then chain this together to create sentences. For example, seeding the model with "START I want to be" might predict the next word as "the." Note: START is a special token I use to signify the beginning of a sentence. END is also a special token to specify the end of a sentence. Then using, "I want to be the", perhaps my model would predict "President." Lastly, given, "want to be the President" my model could predict END. This would then be the end of a sentence - "I want to be the President."
                </p>
                <p className="bold-p"> 
                    To let others experiment with this model, I developed the web app seen above. This app will produce a single sentence give 4 seed words (only 4 because the first is the START token). One can input any 4 words (space separated) and see what is produced. If you try using a word not in the vocabulary, an error will be returned. Or you can have some seed words generated for you. You can also specify a diversity value (the slider). Increasing the value, creates sentences with more diverse word selections. It should be noted that my model currently suffers from a lack of data and not a lot of training. I am working on fixing the latter. I wanted to make sure I could get this web app working first, and now that it is, I will upload some better weights once I do some more training. 
                </p>
            </div>
        );
    }
});

ReactDOM.render(
    <PresApp />,
    document.getElementById('content')
);
