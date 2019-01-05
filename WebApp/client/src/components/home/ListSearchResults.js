import React, {Component} from "react";
import {Container, ListGroup, ListGroupItem, Button} from "reactstrap";
import {CSSTransition, TransitionGroup} from "react-transition-group";

// muss importiert werden, da wir redux verwenden
import {connect} from "react-redux";
import {getPages, deletePage} from "../../actions/pageActions"
import PropTypes from "prop-types"

class ListSearchResults extends Component{


    render(){
            const searchResultItem = this.props.search.map(result => (
            <ListGroupItem className="my-3">
{/*              why id.$oid? from python we have to send json to our backend
             due to zeroRPC or RPC in generall all Attributes have to be serializable
             normally _id not is 123412 ect but _id = ObjectId(123412) and that is not serializable
             so json.utils made it serializable and so _id got converted to _id.$oid */}
            <div key={result._id.$oid}>
                <h5>
                    {result.title}
                </h5>
                <p>{result.date}</p>
                    <p>{result.text}</p>
            </div>
            </ListGroupItem>
        ));

        return (
            <Container className="mt-5">
                <ListGroup>
                        {searchResultItem}
                </ListGroup>
            </Container>
        );
    }
}



const mapStateToProps = (state) => ({
    search: state.search.searchResults
});

export default connect(mapStateToProps,
null // redux mapDispatchToProps in short Object-notation-form
)(ListSearchResults); // die Klasse

