import React, {useState} from "react";
import { Redirect } from "react-router-dom";
import withContext from "../contexts/withProductContext";

const Login = (props) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const changeUsername = e => {
        setUsername(e.target.value);
    }

    const changePassword = e => {
        setPassword(e.target.value);
    }

    const login = e => {
        e.preventDefault();

        if (!username || !password) {
            return setError("Fill all fields!" );
        }
        props.context.login(username, password)
            .then((loggedIn) => {
                if (!loggedIn) {
                    setError("Invalid Credentails");
                }
            })
    };

    return !props.context.user ? (
        <>
            <div className="hero is-primary ">
                <div className="hero-body container">
                    <h4 className="title">Login</h4>
                </div>
            </div>
            <br />
            <br />
            <form onSubmit={login}>
                <div className="columns is-mobile is-centered">
                    <div className="column is-one-third">
                        <div className="field">
                            <label className="label">Username: </label>
                            <input
                                className="input"
                                type="email"
                                name="username"
                                onChange={changeUsername}
                            />
                        </div>
                        <div className="field">
                            <label className="label">Password: </label>
                            <input
                                className="input"
                                type="password"
                                name="password"
                                onChange={changePassword}
                            />
                        </div>
                        {error && (
                            <div className="has-text-danger">{error}</div>
                        )}
                        <div className="field is-clearfix">
                            <button
                                className="button is-primary is-outlined is-pulled-right"
                            >
                                Submit
                            </button>
                        </div>
                    </div>
                </div>
            </form>
        </>
    ) : (
        <Redirect to="/products" />
    );
}

export default withContext(Login);