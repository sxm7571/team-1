import React from "react";
import Context from "./productContext";

const withContext = WrappedComponent => {
    return props => {
        return (
            <Context.Consumer>
                {context => <WrappedComponent {...props} context={context}/>}
            </Context.Consumer>
        );
    };
};

export default withContext;