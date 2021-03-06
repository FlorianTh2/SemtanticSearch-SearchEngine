// Was passiert hier? der PageReducer stellt Methoden bereit, um den internal state zu manipulieren

import {GET_MOSTOFTENSEARCHED} from "../actions/types";


const initialState = {
    readTime: {}
}

export default function(state = initialState, action){ // diese 2 Parameter müssen genau so heißen und sind nicht optional
    switch(action.type){
        // returns the state from the store
        case GET_MOSTOFTENSEARCHED:
            return {
                ...state,
                results: action.payload
            };
        default:
            return state;
    }

}