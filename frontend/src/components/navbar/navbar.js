import React from "react";
import Logo from "../logo/logo";

import "./navbar.css";

function Navbar(props) {
    const classes = "navbar " + props.className;

    return (
        <div className={classes}>
            <Logo />
        </div>
    );
}

export default Navbar;
