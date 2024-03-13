import React from "react";
import { Link } from "react-router-dom";
import Logo from "../../components/logo/logo";

import "./Layout.css"

function Layout() {
    return(
        <div className="container">
            <Logo className="black" />
            <Link to="/teste"><h1>Hello World!</h1></Link>
            <p>PS: Só queria mostrar que sei centralizar div ^^</p>
        </div>
    )
}

export default Layout
